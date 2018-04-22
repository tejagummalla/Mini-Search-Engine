import com.sun.org.apache.xpath.internal.operations.Bool;

import java.io.*;

/**
 * Created by shail on 12/08/16.
 */
public class Precision {
    public static void main(String args[]) throws IOException {
        String filename = "lucene_result.txt";
        String line;
        FileReader fileReader = new FileReader(filename);
        BufferedReader bufferedReader = new BufferedReader(fileReader);
        PrintStream out = new PrintStream(new FileOutputStream("lucene_result2.txt"));
        int match = 0;
        float precision = 0;
        float recall = 0;
        boolean isRel;
        int a[] = {5, 3, 6, 12, 8, 3, 28, 3, 9, 35, 19, 5, 11, 44, 10, 17, 16, 11, 11, 3, 11, 17, 4, 13, 51, 30, 29, 5, 19, 4, 2, 3, 1, 0, 0, 20, 12, 16, 12, 10, 0, 21, 41, 17, 26, 0, 0, 12, 8, 0, 0, 0, 0, 0, 0, 0, 1, 30, 43, 27, 31, 8, 12, 1};
        while((line = bufferedReader.readLine()) != null) {
            String[] data = line.split("\t");

            int q_no = Integer.parseInt(data[0]);
            int total_rel = a[q_no-1];
            if(total_rel==0) continue;
            int rank = Integer.parseInt(data[3]);
            if(rank == 1) match = 0;

            if(data[6].equals("R"))
                isRel = true;
            else isRel = false;

            if(isRel)
                match = match +1;

            precision = (float)match/(float)rank;
            recall = (float)match/total_rel;
            out.println(line+"\t"+precision+"\t"+recall);
        }
    }
}