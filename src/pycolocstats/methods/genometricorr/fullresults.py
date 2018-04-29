import re


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
    filedesc = open(file, "r")
    results_by_string = filedesc.read().split("\n")
    first = 1
    data = []  # to append
    fieldnames = []  # to append
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
    chrnames.pop(awhole)  # genomewide

    tuplovoz = []
    for n, chrom in enumerate(chrnames):
        tuplovoz.append((chrom, n))

    tuplovoz = sorted_nicely_tup(tuplovoz)

    # gather the table
    table = "<table><tr><th></th>"
    table += "<th>All</th>"
    for tup in tuplovoz:
        table += "<th>" + tup[0] + "</th>"
    table += "</tr>\n"
    for row, name in enumerate(fieldnames):
        table += "<tr>"
        table += "<td>" + name + "</td>"
        table += "<td>" + scissors(data[row][awhole]) + "</td>"
        for tup in tuplovoz:
            table += "<td>" + scissors(data[row][tup[1]]) + "</td>"
        table += "</tr>\n"

    table += "</table>\n"
    return table


# print tuplovoz
# print fieldnames
# print data


def gc_html(outputFolder=None, stdoutFile=None, stderrFile=None):
    html = "<!DOCTYPE html>\n"
    html += "<html>\n"
    html += "<head>\n"
    html += "<style>\n"
    html += "td {\n"
    html += "\twhite-space: nowrap;\n"
    html += "}\n"
    html += "th {\n"
    html += "\ttext-align: left;\n"
    html += "}\n"
    html += "table {\n"
    html += "\tborder-spacing: 5px;\n"
    html += "}\n"
    html += "</style>\n"
    html += "<title>GenometriCorr results</title>\n"
    html += "</head>\n"
    html += "<body>\n"
    html += "<h3> GenometriCorr results: </h3>\n"
    html += output_to_table(outputFolder + "/GenometriCorr_Output.txt")
    html += "<p>Please refer to <a href=http://genometricorr.sourceforge.net/GenometriCorr.pdf> GenometriCorr documentaion </a></p>\n"
    html += "<h3> Technical information: </h3>\n"
    html += "<p><a href = \"" + outputFolder + "/conf.ini\"> Configuration file </a></p>\n"
    html += "<p><a href = \"" + outputFolder + "/genometricorr.r\"> R calling code </a></p>\n"
    html += "<p><a href = \"" + stdoutFile + "\">stdout</a></p>\n"
    html += "<p><a href = \"" + stderrFile + "\">stderr</a></p>\n"
    html += "</body>"
    html += "</html>"
    return html

