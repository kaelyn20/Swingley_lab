library(dada2)
path <- "Swingley-lab/dada2/Nachusa_FC_2018/fastas"
list.files(path)

#inspect and read quality profiles
fnFs <- sort(list.files(path, pattern = "_R1_001.fastq", full.names=TRUE))
fnRs <- sort(list.files(path, pattern = "_R2_001.fastq", full.names = TRUE))

sample.names <- sapply(strsplit(basename(fnFs), "_"), '[', 1)

plotQualityProfile(fnFs[1:2])
plotQualityProfile(fnRs[1:2])

#filter and trim
filtFs <- file.path(path, "filtered", paste0(sample.names, "_F_filt.fastq"))
filtRs <- file.path(path, "filtered", paste0(sample.names, "_R_filt.fastq"))
names(filtFs) <- sample.names
names(filtRs) <- sample.names

out <- filterAndTrim(fnFs, filtFs, fnRs, filtRs, maxN=0, maxEE=c(2,2), truncQ = 2, rm.phix = TRUE, compress = TRUE, multithread = FALSE)
head(out)

#learning the error rates
errF <- learnErrors(filtFs, multithread= FALSE)
errR <- learnErrors(filtRs, multithread = FALSE)
plotErrors(errF, nominalQ= TRUE)

#sample inference
dadaFs <- dada(filtFs, err=errF, multithread = FALSE)
dadaRs <- dada(filtRs, err=errR, multithread = FALSE)

dadaFs[[1]]

#merge paired reads
mergers <- mergePairs(dadaFs, filtFs, dadaRs, filtRs, verbose = TRUE)
  #inspect merger data.frame from first sample
head(mergers[[1]])


#construct sequence table
seqtab <- makeSequenceTable(dadaFs)
dim(seqtab)
  #inspect distribution of sequence lengths
table(nchar(getSequences(seqtab)))

#remove chimeras
seqtab.nochim <- removeBimeraDenovo(seqtab, method ="consensus", multithread = FALSE, verbose = TRUE)
dim(seqtab.nochim)
sum(seqtab.nochim)/sum(seqtab)

#track reads through pipeline
getN <- function(x) sum(getUniques(x))
track <- cbind(out, sapply(dadaFs, getN), rowSums(seqtab.nochim))
colnames(track) <- c("input", "filtered", "denoisedF", "nochim")
rownames(track) <- sample.names
head(track)

#assign taxonomy
taxa <- assignTaxonomy(seqtab.nochim, "Swingley-lab/dada2/Nachusa_FC_2018/silva_nr_v132_train_set.fa.gz", multithread = FALSE)
taxa.print <- taxa
rownames(taxa.print) <-NULL
head(taxa.print)

write.csv(taxa, "Swingley-lab/dada2/Nachusa_FC_2018/out.csv")
