#!/usr/bin/python
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import os

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_rules_clang_doc():
    warning_list_slices = []
    clang_diagnostic_url = 'http://releases.llvm.org/5.0.0/tools/clang/docs/DiagnosticsReference.html'
    diagnostic_page = requests.get(clang_diagnostic_url)
    diagnostic_content = diagnostic_page.content
    soup = BeautifulSoup(diagnostic_content, 'lxml')
    warnings_list = soup.find('div', {'class':'section', 'id':'diagnostic-flags'}).findAll('h3')
    for warning in warnings_list:
        warning_list_slices.append(removeNonAscii(warning.text))
    return warning_list_slices

def get_rules_nonofficial_doc():
    warning_list_slices = []
    clang_warnings_url = 'http://fuckingclangwarnings.com/'
    warnings_page = requests.get(clang_warnings_url)
    warnings_content = warnings_page.content
    soup = BeautifulSoup(warnings_content, 'lxml')
    warning_list = soup.find('div', {'id':'main'}).findAll('td', {'itemprop':'name'})
    for warning in warning_list:
        warning_list_slices.append(warning.text)
    return warning_list_slices

if __name__ == '__main__':
    warnings_official = get_rules_clang_doc()

    file = open('sonar_rules', 'w')

    file.writelines('<rules>\n')

    for warning in warnings_official:
        file.write('  <rule>\n')
        file.write('    <key>{}-clang-compiler</key>\n'.format(warning))
        file.write('    <name>{}</name>\n'.format(warning))
        file.write('    <description>Clang compiler warning, message will contain additional description</description>\n')
        file.write('    <severity>Minor</severity>\n')
        file.write('    <type>BUG</type>\n')
        file.write('  </rule>\n')

    file.write('</rules>\n')