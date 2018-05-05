import re
from os import linesep

from pycolocstats.core.constants import CWL_OUTPUT_FOLDER_NAME
from pycolocstats.core.util import getLastTwoPartsOfFilePath


def sorted_nicely(
        l):  # code from https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def sorted_nicely_tup(
        l):  # code from https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    alphanum_key_tup = lambda tup: alphanum_key(tup[0])
    return sorted(l, key=alphanum_key_tup)


def scissors(q):  # trim float values
    try:
        f = float(q)
    except ValueError:
        return q  # non-numeric
    if f == int(f):  # int
        return q
    return "{0:.3g}".format(f)  # float


def output_to_table(file):
    chrnames = []
    results_by_string = []
    with open(file, "rt") as filedesc:
        results_by_string = [x.strip() for x in filedesc.readlines()]
    # filedesc = open(file, "rt")
    # results_by_string = filedesc.read().split("\n")
    first = 1
    data = []  # to append
    fieldnames = []  # to append
    awhole = None
    for typeline in results_by_string:
        dataline = typeline.split("\t")
        if len(dataline) <= 1:
            continue
        if first:
            first = 0
            chrnames = dataline[1:]
            for n, chrom in enumerate(chrnames):
                if chrom == "awhole":
                    awhole = n  # it is not to be sorted at all, the last line in table
                    break
        else:  # not first line
            if dataline[0] == "relative.distances.ecdf.deviation.area":
                continue
            if dataline[0] == "scaled.absolute.min.distance.sum":
                continue
            fieldnames.append(dataline[0])
            data.append(dataline[1:])
    if awhole is not None and chrnames:
        chrnames.pop(awhole)  # genomewide

    tuplovoz = []
    for n, chrom in enumerate(chrnames):
        tuplovoz.append((chrom, n))

    tuplovoz = sorted_nicely_tup(tuplovoz)

    # gather the table
    table = "<table>"
    if tuplovoz and fieldnames and data:
        table += "<tr><th></th>"
        table += "<th>All</th>"
        for tup in tuplovoz:
            table += "<th>" + tup[0] + "</th>"
        table += "</tr>" + linesep
        for row, name in enumerate(fieldnames):
            table += "<tr>"
            table += "<td>" + name + "</td>"
            table += "<td>" + (scissors(data[row][awhole]) if awhole is not None else "N/A") + "</td>"
            for tup in tuplovoz:
                table += "<td>" + scissors(data[row][tup[1]]) + "</td>"
            table += "</tr>" + linesep

    table += "</table>" + linesep
    return table


# print tuplovoz
# print fieldnames
# print data


def gc_html(outputFolder=None, stdoutFile=None, stderrFile=None):
    from os.path import sep
    rootFolderName = outputFolder.split(sep)[-1] if outputFolder else ""
    stdoutRelPath = getLastTwoPartsOfFilePath(stdoutFile)
    stderrRelPath = getLastTwoPartsOfFilePath(stderrFile)

    html = "<!DOCTYPE html>" + linesep
    html += "<html>" + linesep
    html += "<head>" + linesep
    html += "<style>" + linesep
    html += "td {" + linesep
    html += "\twhite-space: nowrap;" + linesep
    html += "}" + linesep
    html += "th {" + linesep
    html += "\ttext-align: left;" + linesep
    html += "}" + linesep
    html += "table {" + linesep
    html += "\tborder-spacing: 5px;" + linesep
    html += "}" + linesep
    html += "</style>" + linesep
    html += "<title>GenometriCorr results</title>" + linesep
    html += "</head>" + linesep
    html += "<body>" + linesep
    html += "<h3> GenometriCorr results: </h3>" + linesep
    html += output_to_table(outputFolder + sep + "GenometriCorr_Output.txt")
    html += "<p>Please refer to <a href=http://genometricorr.sourceforge.net/GenometriCorr.pdf> GenometriCorr documentaion </a></p>" + linesep
    html += "<h3> Technical information: </h3>" + linesep
    html += "<p><a href = \"" + CWL_OUTPUT_FOLDER_NAME + sep + rootFolderName + sep + "conf.ini\"> Configuration file </a></p>" + linesep
    html += "<p><a href = \"" + CWL_OUTPUT_FOLDER_NAME + sep + rootFolderName + sep + "genometricorr.r\"> R calling code </a></p>" + linesep
    html += "<p><a href = \"" + CWL_OUTPUT_FOLDER_NAME + sep + stdoutRelPath + "\">stdout</a></p>" + linesep
    html += "<p><a href = \"" + CWL_OUTPUT_FOLDER_NAME + sep + stderrRelPath + "\">stderr</a></p>" + linesep
    html += "</body>"
    html += "</html>"
    return html


