#Load Dada2 package
library(dada2); packageVersion("dada2")

#Sets the working directory 
setwd ("~/Swingley-lab/dada2/Nachusa_HN/")
path <- "~/Swingley-lab/dada2/Nachusa_HN"

#View files
list.files(path)

# Forward and reverse fastq filenames have format: SAMPLENAME_R1_001.fastq and SAMPLENAME_R2_001.fastq
fnFs <- sort(list.files(path, pattern="_nonchimeras.fastq", full.names = TRUE))

# Extract sample names, assuming filenames have format: SAMPLENAME_XXX.fastq
sample.names <- sapply(strsplit(basename(fnFs), "_nonchimeras.fastaq"), `[`, 1)

#View the plots and and check quality scores
plotQualityProfile(fnFs[1:2])


# Place filtered files in filtered/ subdirectory
filtFs <- file.path(path, "filtered", paste0(sample.names, "_F_filt.fastq.gz"))
names(filtFs) <- sample.names


#filter and trim files based on quality scores and other metrics 
out <- filterAndTrim(fnFs, filtFs, 
                     maxN=0, maxEE=2, truncQ=2, rm.phix=TRUE,
                     compress=TRUE, multithread=FALSE)

#learn error rates
errF <- learnErrors(filtFs, multithread=TRUE)


#Visualuze error rates
plotErrors(errF, nominalQ=TRUE)

#sample inference
dadaFs <- dada(filtFs, err=errF, multithread=TRUE)


#Construct Sequence table 
seqtab <- makeSequenceTable(dadaFs)
dim(seqtab)

# Inspect distribution of sequence lengths
table(nchar(getSequences(seqtab)))

#Remove Chimera's
seqtab.nochim <- removeBimeraDenovo(seqtab, method="consensus", multithread=TRUE, verbose=TRUE)
dim(seqtab.nochim)

#Checks the proprtion of chimeras removed to the original file 
sum(seqtab.nochim)/sum(seqtab)



#Assign taxonomy using silva database
taxa2 <- assignTaxonomy(seqtab.nochim, "~/Swingley-lab/dada2/Nachusa_FC_2018/silva_nr_v132_train_set.fa.gz", multithread=FALSE)



#Call libraries to generate plots for analyzing abundance 
library(phyloseq); packageVersion("phyloseq")
library(Biostrings); packageVersion("Biostrings")
library(ggplot2); packageVersion("ggplot2")
theme_set(theme_bw())

#Organize data
samples.out <- rownames(seqtab.nochim)
subject <- sapply(strsplit(samples.out, "-"), `[`, 1)
time <- sapply(strsplit(samples.out, "N"), `[`, 2)
temptime <- as.integer(substr(time, 2, 3))

for(i in 1:length(temptime)) {
  if(temptime[i] > 12) {
      mon <- as.integer(substr(time, 4, 5))
  }
  else {
    mon2 <- as.integer(substr(time, 2, 3))
  }
}

samdf <- data.frame(Subject=subject, Month=test)
samdf$Season[samdf$Month >=3] <- "20"
samdf$Season[samdf$Year == 14] <- "2014"
samdf$Season[samdf$Year == 19] <- "2019"
rownames(samdf) <- samples.out

#Contruct phyloseq object 
ps <- phyloseq(otu_table(seqtab.nochim, taxa_are_rows=FALSE), 
               sample_data(samdf), 
               tax_table(taxa2))

dna <- Biostrings::DNAStringSet(taxa_names(ps))
names(dna) <- taxa_names(ps)
ps <- merge_phyloseq(ps, dna)
taxa_names(ps) <- paste0("ASV", seq(ntaxa(ps)))
ps

#Visualize alpha diversity
plot_richness(ps, x="Month", measures=c("Shannon", "Simpson"), color="Season")

# Transform data to proportions as appropriate for Bray-Curtis distances
ps.prop <- transform_sample_counts(ps, function(otu) otu/sum(otu))
ord.nmds.bray <- ordinate(ps.prop, method="NMDS", distance="bray")

plot_ordination(ps.prop, ord.nmds.bray, color="When", title="Bray NMDS")

#Barplot
top20 <- names(sort(taxa_sums(ps), decreasing=TRUE))[1:20]
ps.top20 <- transform_sample_counts(ps, function(OTU) OTU/sum(OTU))
ps.top20 <- prune_taxa(top20, ps.top20)
plot_bar(ps.top20, x="Month", fill="Phylum") + facet_wrap(~Season, scales="free_x")

write.csv(taxa2, "Swingley-lab/dada2/Nachusa_HN/taxatable.csv")


top30 <- names(sort(taxa_sums(ps), decreasing=TRUE))[1:30]
ps.top30 <- transform_sample_counts(ps, function(OTU) OTU/sum(OTU))
ps.top30 <- prune_taxa(top30, ps.top30)
plot_bar(ps.top30, x="Month", fill="Phylum") + facet_wrap(~Season, scales="free_x")

