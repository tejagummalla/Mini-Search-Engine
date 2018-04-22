import java.io.*;
import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Searcher {
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);
    private static  int NO_OF_RESULTS = 100;

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    Searcher(String indexDir) throws IOException {
        FSDirectory dir = FSDirectory.open(new File(indexDir));
        IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);
        writer = new IndexWriter(dir, config);
    }

    public static void main(String[] args) throws IOException, ParseException {

        String indexLocation = "index3";
        String s = indexLocation;

        Searcher indexer = null;
        try {
            indexLocation = s;
            indexer = new Searcher(s);
        } catch (Exception ex) {
            System.out.println("Cannot create index..." + ex.getMessage());
            System.exit(-1);
        }

        // ===================================================
        // read input from user until he enters q for quit
        // ===================================================
        indexer.indexFileOrDirectory("cacm");

        // ===================================================
        // after adding, we always have to call the
        // closeIndex, otherwise the index is not created
        // ===================================================
        indexer.closeIndex();

        // =========================================================
        // Now search
        // =========================================================
        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
                indexLocation)));
        IndexSearcher searcher = new IndexSearcher(reader);
        String queryFile = "queries.txt";
        BufferedReader br2 = new BufferedReader(new FileReader(queryFile));
        String qs;
        int count = 0;
        PrintStream out = new PrintStream(new FileOutputStream("lucene_result.txt"));
        while ((qs = br2.readLine()) != null) {
            qs = qs.toLowerCase();
            count++;
            qs.replaceFirst("[0-9]+ ", "");
            Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(QueryParser.escape(qs));
            //searcher.search(q, collector);
            //ScoreDoc[] hits = collector.topDocs().scoreDocs;
            TopDocs docs = searcher.search(q, NO_OF_RESULTS);
            ScoreDoc[] hits = docs.scoreDocs;

            // 4. display results
            //System.out.println("Found " + hits.length + " hits.");
            for (int i = 0; i < hits.length; ++i) {
                //if(i%2==1) continue;
                int docId = hits[i].doc;
                Document d = searcher.doc(docId);
                String currFile = d.get("path");
                currFile = currFile.substring(currFile.indexOf("\\")+1, currFile.indexOf("."));
                //int currRank = (i/2)+1;
                int currRank = (i+1);
                out.println(count +"\tQ0\t" +currFile+"\t"+ currRank + "\t" + hits[i].score + "\t" + "LUCENE");
            }
        }
    }

    /**
     * Constructor
     *
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */


    /**
     * Indexes a file or directory
     *
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
        // ===================================================
        // gets the list of files in a folder (if user has submitted
        // the name of a folder) or gets a single file name (is user
        // has submitted only the file name)
        // ===================================================
        addFiles(new File(fileName));

        int originalNumDocs = writer.numDocs();
        for (File f : queue) {
            FileReader fr = null;
            try {
                Document doc = new Document();

                // ===================================================
                // add contents of file
                // ===================================================
                fr = new FileReader(f);
                doc.add(new TextField("contents", fr));
                doc.add(new StringField("path", f.getPath(), Field.Store.YES));
                doc.add(new StringField("filename", f.getName(),
                        Field.Store.YES));

                writer.addDocument(doc);
                System.out.println("Added: " + f);
            } catch (Exception e) {
                System.out.println("Could not add: " + f);
            } finally {
                fr.close();
            }
        }

        int newNumDocs = writer.numDocs();
        System.out.println("");
        System.out.println("************************");
        System.out.println((newNumDocs - originalNumDocs) + " documents added.");
        System.out.println("************************");

        queue.clear();
    }

    private void addFiles(File file) {

        if (!file.exists()) {
            System.out.println(file + " does not exist.");
        }
        if (file.isDirectory()) {
            for (File f : file.listFiles()) {
                addFiles(f);
            }
        } else {
            String filename = file.getName().toLowerCase();
            // ===================================================
            // Only index text files
            // ===================================================
            if (filename.endsWith(".htm") || filename.endsWith(".html") || filename.endsWith(".xml") || filename.endsWith(".txt")) {
                queue.add(file);
            } else {
                System.out.println("Skipped " + filename);
            }
        }
    }

    /**
     * Close the index.
     *
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
        writer.close();
    }
}