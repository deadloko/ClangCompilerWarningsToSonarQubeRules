#! /usr/bin/python

from xml.sax.saxutils import escape
import re

def ConvertDiagnosticLineToSonqarqube(item):
    try:
        id, line, message, source_file = GetDiagnosticFieldsFromDiagnosticLine(item)
        WriteDiagnosticFieldsToFile(id, line, message, source_file)
    except:
        print 'Cant parse line {}'.format(item)


def GetDiagnosticFieldsFromDiagnosticLine(item):
    source_file = re.search('\/(.*?):', item).group(0).replace(':', '')
    line = re.search(':\d*:', item).group(0).replace(':', '')
    id = re.search('\[.*\]', item).group(0).replace('[', '').replace(']', '') + '-clang-compiler'
    message = re.search('warning: (.*)\[', item).group(0).replace('[', '').replace('warning: ', '')
    return id, line, message, source_file


def WriteDiagnosticFieldsToFile(id, line, message, source_file):
    clang_sonar_report.write(" <error file=\"" + str(source_file) +
                        "\" line=\"" + str(line) +
                        "\" id=\"" + str(id) +
                        "\" msg=\"" + escape(str(message)) + "\"/>\n")


def CreateOutputFile():
    file_to_write = open('clang_compiler_report.xml', 'w')
    file_to_write.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    file_to_write.write('<results>\n')
    return file_to_write


def ReadCompilerReportFile():
    file = open('clang_compiler_report_formatted', 'r')
    messages_xml = file.readlines()
    return messages_xml


def CloseOutputFile():
    clang_sonar_report.write('</results>\n')
    clang_sonar_report.close()


def WriteSonarRulesToOutputFile():
    item_list = clang_compiler_report
    for item in item_list:
        ConvertDiagnosticLineToSonqarqube(item)


if __name__ == '__main__':
    clang_sonar_report = CreateOutputFile()
    clang_compiler_report = ReadCompilerReportFile()

    WriteSonarRulesToOutputFile()
    CloseOutputFile()
