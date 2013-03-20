#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cm_util import *
from cm_contacts import *
from cm_perm_tidy import *
from cm_perm_fact import *
from cm_perm_maps import *

import sys
print sys.getdefaultencoding()
import sqlite3
import urlparse
import urllib
import codecs
import cm_contacts

print "start"
db = sqlite3.connect('db_app.db')

#######################################


from Bio import SeqIO
from Bio import motifs
from Bio.Cluster import distancematrix
from Bio.Cluster import clustercentroids
records = list(SeqIO.parse("./txt/cm_perm_sequence_27_social.fasta", "fasta"))
for seq_record in SeqIO.parse("./txt/cm_perm_sequence_27_social.fasta", "fasta"):
    print seq_record.id
    print repr(seq_record.seq)
    print len(seq_record)
from Bio.Align.Applications import ClustalwCommandline
clustalx = '/Applications/PhylogeneticAnalysis/clustalw2'
cline = ClustalwCommandline(clustalx, infile="./txt/cm_perm_sequence_27_social.fasta")
print cline
stdout, stderr = cline()
from Bio import Phylo
tree = Phylo.read("./txt/cm_perm_sequence_27_social.dnd", "newick")
tree.rooted = True
#Phylo.draw(tree)

from ete2 import Tree
from ete2 import PhyloTree
t = PhyloTree('./txt/cm_perm_sequence_27_social.dnd')
t.link_to_alignment(alignment="./txt/cm_perm_sequence_27_social.fasta", alg_format="fasta")
#from ete2 import ClusterTree
#t = ClusterTree('./txt/cm_perm_sequence_27_social.dnd')
t.show()
#t.show("heatmap")
#t.show("cluster_cbars")
#t.show("cluster_bars")
#t.show("cluster_lines")
