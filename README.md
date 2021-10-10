# GPoeTry

While on a long drive, my brother and I ended up betting about whether "AI" will ever be able to produce poetry that a human reader - specifically my brother - won't be able to tell from human-written poetry. This is the code to run that experiment.

## Rules

Here's the rules we agreed on:

1. The "Human" poems will be sourced from some online collection of public domain poems, and will be grouped by author.
2. The "AI" poems can look at the "Human" poems by an author when generating their poems.
3. The test is given by pairing one "Human" and one "AI" poem from a set of random authors, and testing how frequently my brother picks the right poem.

## This Repo

There are three parts to this repo.

- ingestion: downloads/formats "human" poems
- generation: creates "AI" poems using the "human" poems
- experiment: runs the test described above using the two sets of poems