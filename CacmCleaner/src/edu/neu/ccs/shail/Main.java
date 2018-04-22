package edu.neu.ccs.shail;

import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.*;
import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    private static String removePunctuation(String txt){
        txt = txt.replaceAll("\\[([0-9]+)\\]", " "); //remove annoying reference links like [1]
        txt = txt.replaceAll("[/]", " "); // replace / with a space. so boy/girl is not boygirl
        String word[] = txt.split(" ");     // parse word by word
        for(int i = 0; i < word.length; i++){
            if(word[i].matches(".*\\d.*"))
                word[i] = word[i].replaceAll("[^A-Za-z0-9-.,:]", ""); //retain the dots and commas
            else word[i] = word[i].replaceAll("[^A-Za-z0-9-]", " "); //retain the -
            word[i] = word[i].replaceAll(",$" ," "); //if the word ends in a ,, delete it
            if(word[i].length() == 2) word[i] = word[i];
            else word[i] = word[i].replaceAll("\\.$" ," "); // if the word ends in a ., delete it
            word[i] = word[i].replaceAll("-$" ," "); //if the word ends in a -, delete it
            word[i] = word[i].replaceAll("-", " "); // if the word is only a -, delete it
            word[i] = word[i].replaceAll("('s)"," "); // remove 's
            //word[i] = word[i].replaceAll("(^| )[b-z]( |$)", " "); // remove single alphabets, except a
        }
        String returnString = String.join(" ", word).replaceAll("\\s{2,}", " ").trim();
        return returnString;
    }

    static void write_to_file(String filename, String text) throws FileNotFoundException, UnsupportedEncodingException {
        PrintWriter writer = new PrintWriter(filename, "UTF-8");
        writer.println(text);
        writer.close();
    }

    static void clean_corpus(String foldername) throws IOException {
        File folder = new File(foldername);
        for (final File fileEntry : folder.listFiles()) {
            if (fileEntry.isDirectory()) {
                clean_corpus(fileEntry.getName());
            } else {
                String filename = fileEntry.getName();
                BufferedReader br = new BufferedReader(new FileReader (foldername+"/"+filename));
                String text;
                StringBuilder sb = new StringBuilder();
                while ((text = br.readLine().toLowerCase()) != null) {

                    if(text.contains("html>")) continue;
                    else if(text.contains("pre>")) continue;
                    else if (text.equals("")) continue;
                    text = removePunctuation(text);

                    sb = sb.append(text+" ");

                    String pattern = "ca[0-9]+";
                    Pattern r = Pattern.compile(pattern);
                    Matcher m = r.matcher(text);
                    if(m.find()) break;
                }
                filename = filename.replace(".html", ".txt");
                System.out.println(filename);
                write_to_file(foldername+"_cleaned/"+filename, sb.toString());
                br.close();
            }
        }
    }
    static void  clean_query(String filename){
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        factory.setNamespaceAware(true);
        DocumentBuilder builder;
        Document doc;
        try {
            builder = factory.newDocumentBuilder();
            doc = builder.parse(filename);
            XPathFactory xpathFactory = XPathFactory.newInstance();
            XPath xpath = xpathFactory.newXPath();
            for(int i = 1; i <= 64; i++) {
                String name = get_content(doc, xpath, i);
                System.out.println(i+" "+name);
            }
    } catch (SAXException e) {
            e.printStackTrace();
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static String get_content(Document doc, XPath xpath, int id){
        String name = null;
        try {
            XPathExpression expr = xpath.compile("/DOCS/DOC["+id+"]/text()");
            name = (String) expr.evaluate(doc, XPathConstants.STRING);
        } catch (XPathExpressionException e) {
            e.printStackTrace();
        }
        return name.trim();
        //return removePunctuation(name.trim()).toLowerCase();
    }

    static void write_stemmed_docs(String filename){
        try {
            BufferedReader br = new BufferedReader(new FileReader (filename));
            String text;
            int count = 0;
            while ((text = br.readLine()) != null) {
                if(text.matches("# [0-9]+")){
                    count++;
                    String num = ""+count;
                    System.out.println(text);
                    while(num.length()<4) num = "0"+num;
                    System.out.println(num);
                    String text2;
                    String to_file="";
                    while(true){
                        text2 = br.readLine();
                        if(text2.endsWith("pm")||text2.endsWith("am")) {
                            to_file = to_file + text2;
                            System.out.println(to_file);
                            write_to_file("cacm_stemmed/CACM-" + num + ".txt", to_file);
                            break;
                        }
                        if(text2.matches("\n")) continue;
                        else to_file = to_file + text2 + " ";
                        //System.out.println(text2);
                    }
                }
                else{
                    System.out.println("Not Matched");
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) throws IOException {
        //clean_corpus("cacm");
        clean_query("cacm_query.txt");
        //write_stemmed_docs("stemed_corpus.txt");
    }
}

/*preprocessing on cacm.query:*/
//Replace <DOCNO> [0-9]+ </DOCNO> with ""
//Replace ^\n with ""
//Replace " " with ""