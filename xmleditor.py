import xml.etree.ElementTree as ET
import codecs
from xml.etree.ElementTree import fromstring, tostring

def main():

    tree = ET.parse('test/xml/TestAdcModel_8c.xml')
    root = tree.getroot()

    # 要素を削除する
    for compounddef in root.findall('compounddef'):
        for programlisting in compounddef.findall('programlisting'):
            compounddef.remove(programlisting) 
        for programlisting in compounddef.findall('includes'):
            compounddef.remove(programlisting) 
        for programlisting in compounddef.findall('incdepgraph'):
            compounddef.remove(programlisting) 
        for sectiondef in compounddef.findall('sectiondef'):
            for memberdef in sectiondef.findall('memberdef'):
                for type in memberdef.findall('type'):
                    memberdef.remove(type) 
                for node in memberdef.findall('node'):
                    memberdef.remove(node) 
                for param in memberdef.findall('param'):
                    memberdef.remove(param) 
                for definition in memberdef.findall('definition'):
                    memberdef.remove(definition) 
                for argsstring in memberdef.findall('argsstring'):
                    memberdef.remove(argsstring) 
                for location in memberdef.findall('location'):
                    memberdef.remove(location) 
                for briefdescription in memberdef.findall('briefdescription'):
                    for listitem in briefdescription.iter('listitem'):
                        for para in listitem.findall('para'):
                            para.text = '- ' + para.text
                for detaileddescription in memberdef.findall('detaileddescription'):
                    for listitem in detaileddescription.iter('listitem'):
                        for para in listitem.findall('para'):
                            para.text = '- ' + para.text

    tree.write('after.xml')

    with open('after.xml', encoding='utf-8') as reader:
        content = reader.read()

    content = content.replace('<itemizedlist>', '')
    content = content.replace('</itemizedlist>', '')
    content = content.replace('<listitem><para>', '')
    content = content.replace('</para>\n</listitem>', '\n')
    content = content.replace('<verbatim>', '')
    content = content.replace('</verbatim>', '')

    with open('after2.xml', 'w', encoding='utf-8') as writer:
        writer.write(content)

if __name__ == '__main__':
    main()

