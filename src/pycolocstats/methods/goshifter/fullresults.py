# python2.7 script to create graphical representations of the results provided in Goshifter in the COLOC-STATS webtool
##By Lara Bossini-Castillo (lbc@sanger.ac.uk). Trynka group. Wellcome Trust Sanger Institute. Hinxton UK
###25th April 2018

import os  # using operating system dependent functionality
import os.path  # common pathname manipulations
import getopt
import sys  # access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter
# import re  # provides regular expression matching operations similar to those found in Perl
# import subprocess  # keeps command output
import time  # time-related functions
#  Import graphic modules
import math
import numpy as np
import pandas as pd
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt

TEMP_FILE_PREFIX = 'goshifter_temp'


def modifyinputs(outputFolder, stdoutFile, stderrFile):  # Read standard output file and modify

    # print(outputFolder)
    # print(stdoutFile)
    # print(stderrFile)
    cmd = 'grep \"p-value = \" %s > %s 2>/dev/null' % (stdoutFile, outputFolder + os.sep + TEMP_FILE_PREFIX + '1.txt')
    os.system(cmd)

    cmd = 'grep \"annotation \" %s > %s 2>/dev/null' % (stdoutFile, outputFolder + os.sep + TEMP_FILE_PREFIX + '2.txt')
    os.system(cmd)

    cmd = 'paste %s %s > %s 2>/dev/null' % (
    outputFolder + os.sep + TEMP_FILE_PREFIX + '1.txt', outputFolder + os.sep + TEMP_FILE_PREFIX + '2.txt', outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)

    cmd = 'vim -c\"%%s/\\s\\+/\\t/g|wq\" %s 2>/dev/null' % (outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)

    cmd = 'vim -c\"%%s/--annotation\\s\\+.\\+\\//\\t/|wq\" %s 2>/dev/null' % (outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)

    cmd = 'vim -c\"%%s/p-value\\s\\+=\\s\\+//|wq\" %s 2>/dev/null' % (outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)

    cmd = 'vim -c\"1s/\\(.\\+\\)/\Index\tPvalue\\tAnnotation\\r1\\t\\1/|wq\" %s 2>/dev/null' % (outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)

    cmd = 'vim -c\"%%s/\\s\\+/\\t/g|wq\" %s 2>/dev/null' % (outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt')
    os.system(cmd)
    return outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt'


def plotting(modified, outputFolder):  # Getting input and plotting
    fname = outputFolder + os.sep + TEMP_FILE_PREFIX + '3.txt'
    results = pd.read_csv(filepath_or_buffer=fname, sep='\t', header=0, index_col=0)
    pvalue = -math.log10(results.iloc[0]['Pvalue'])
    annotation = results.iloc[0]['Annotation']
    N = len([pvalue])
    width = 1 / 1.5
    fname2 = outputFolder + os.sep + 'output.nperm10.locusscore'
    cmd = 'cp %s %s 2>/dev/null' % (fname2, fname2 + '_Copy')
    os.system(cmd)
    cmd = 'vim -c\"%%s/N\/A/0/g|wq\" %s 2>/dev/null' % (fname2 + '_Copy')
    os.system(cmd)
    results2 = pd.read_csv(filepath_or_buffer=fname2 + '_Copy', sep='\t', header=0, index_col=0)
    x1 = results2.loc[:, 'overlap']
    x2 = results2.loc[:, 'score']
    x3 = [np.arange(0, max(x2) + 0.2, 0.1)]
    x4 = np.array(x3).tolist()
    from matplotlib import rcParams
    rcParams['font.family'] = 'serif'
    rcParams['font.serif'] = ['Tahoma']
    import matplotlib.mlab as mlab
    # Turn off display
    plt.ioff()
    # Define plot subplots
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    ax[0].ticklabel_format(useOffset=False)
    ax[0].tick_params(direction='out')
    ax[0].yaxis.set_ticks_position('left')
    ax[0].xaxis.set_ticks_position('bottom')
    ax[0].bar(float(N), pvalue, width, tick_label=float(N), align='center', color='grey')
    ax[0].set_xticklabels(labels=[annotation])
    ax[0].set_yticks(np.arange(0, 4.55, 0.5))
    ax[0].set_ylim([0, 4.5])
    ax[0].set_ylabel('-log10(p-value)')
    ax[0].set_xlabel('Annotation')
    ax[0].set_title('Goshifter enrichment Results')

    # Histogram of the locus overlap
    ax[1].tick_params(direction='out')
    ax[1].yaxis.set_ticks_position('left')
    ax[1].xaxis.set_ticks_position('bottom')
    ax[1].hist(x1, bins=np.arange(0, max(x1) + 2, 1) - 0.5, facecolor='blue', alpha=0.75)
    ax[1].set_xticks(np.arange(0, max(x1) + 2, 1))
    ax[1].set_xticklabels(labels=np.arange(0, max(x1) + 2, 1))
    ax[1].set_ylabel('Number of SNPs')
    ax[1].set_xlabel('Overlaps')
    ax[1].set_title('Goshifter locus overlap')

    # Histogram of the SNP score
    ax[2].tick_params(direction='out')
    ax[2].yaxis.set_ticks_position('left')
    ax[2].xaxis.set_ticks_position('bottom')
    ax[2].hist(x2, bins=np.arange(0, max(x2) + 0.2, 0.1) - 0.05, facecolor='darkblue', alpha=0.75)
    ax[2].set_xticks(np.arange(0, max(x2) + 0.2, 0.1))
    ax[2].set_ylabel('Number of SNPs')
    ax[2].set_xlabel('Score')
    ax[2].set_xticklabels(labels=np.arange(0, max(x2) + 0.2, 0.1))
    ax[2].set_title('Goshifter SNP score')

    # save figure as png
    outputplot = outputFolder + os.sep + 'barplot.png'
    fig.savefig(outputplot)
    plt.close(fig)
    return outputFolder + os.sep + 'barplot.png'


# def HTML(plotted, outputFolder):  # Create HTML file
#     outputhtml = outputFolder + os.sep + 'Goshifter_Result.html'
#     text_file = open(outputhtml, "w")
#     text_file.write(toHtml())
#     text_file.close()
#     return outputFolder + os.sep + 'Goshifter_Result.html'


def toHtml(outputFolder, stdoutFn, stderrFn, pathPrefix=""):
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        modified = modifyinputs(outputFolder, stdoutFn, stderrFn)
        plotted = plotting(modified, outputFolder)
        #clean() #not sure if needed

    rootFolderName = outputFolder.split(os.sep)[-1] if outputFolder else ""

    plotFilePath = pathPrefix + os.sep + rootFolderName + os.sep + "barplot.png"

    from os import linesep
    raw_html = ""
    raw_html += "<html>" + linesep
    raw_html += "\t<body>" + linesep
    raw_html += "\t\t\"<img src=\"" + plotFilePath + "\">" + linesep
    raw_html += "\t</body>" + linesep
    raw_html += "</html>"

    # return "<html>\n\t<body>\n\t\t<img src=\"barplot.png\">\n\t<body>\n<html>"
    return raw_html


def clean():
    cmd = 'rm {}*'.format(TEMP_FILE_PREFIX)
    os.system(cmd)
    cmd = 'rm *_Copy'
    os.system(cmd)
    return
#
#
# if __name__ == '__main__':
#     starttime = time.time()
#     if len(sys.argv) < 1:  # The list of command line arguments passed to a Python script
#         # print (USAGE % sys.argv[0])
#         sys.exit(1)
#
#     opts, args = getopt.getopt(sys.argv[1:], "", ['outputFolder=', 'stdoutFile=', 'stderrFile='])
#     for o, a in opts:
#         if o == '--outputFolder':
#             outputFolder = a
#         if o == '--stdoutFile':
#             stdoutFile = a
#         if o == '--stderrFile':
#             stderrFile = a
#
#     # logfile = open("log.txt", "w")
#     modified = modifyinputs(outputFolder, stdoutFile, stderrFile)
#     plotted = plotting(modified, outputFolder)
#     html = HTML(plotted, outputFolder)
#     clean(html)
#
#     # logfile.close()
#     endtime = time.time()
#     print('it takes %.3f minutes or %.3f seconds' % ((endtime - starttime) / 60, endtime - starttime))
