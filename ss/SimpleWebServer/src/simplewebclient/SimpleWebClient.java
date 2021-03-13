package simplewebclient;

import java.io.*;
import java.net.*;

public class SimpleWebClient {
    private static final String hostName = "localhost";
    private static final int PORT = 8080;

    public static void serveFile(OutputStreamWriter osw, String pathname) throws Exception {
        FileReader fr = null;
        int c = -1;
        StringBuffer sb = new StringBuffer();

        /* try to open file specified by pathname */
        try {
            // System.out.println("Path name: "+pathname);
            fr = new FileReader(pathname);
            c = fr.read();
            System.out.println(c);
        } catch (Exception e) {
            /* if the file is not found,return the appropriate HTTP response code */
            System.out.println("File not found!");
            fr.close();
            return;
        }

        /*
         * if the file can be successfully opened and 
         * read, then send the contents of the file
         */
        while (c != -1) {
            sb.append((char) c);
            c = fr.read();
        }
        osw.write(sb.toString());
    }

    public static void main(String[] args) throws Exception {
        try (Socket serverSocket = new Socket(hostName, PORT);
                OutputStreamWriter osw = new OutputStreamWriter(serverSocket.getOutputStream());
                PrintWriter out = new PrintWriter(serverSocket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(new InputStreamReader(serverSocket.getInputStream()));
                BufferedReader stdIn = new BufferedReader(new InputStreamReader(System.in))) {
            String userInput;
            if ((userInput = stdIn.readLine()) != null) {
                out.println(userInput);
                // checks if the user input contains multiple argument
                if (userInput.contains(" ")) {
                    String reqType = userInput.split(" ")[0];
                    // handle put command
                    if (reqType.equals("PUT")) {
                        String pathname = userInput.split(" ")[1];
                        serveFile(osw, pathname);
                        osw.close();
                    } else if (reqType.equals("GET")) { // handle get command
                        String response=in.readLine();
                        if (response!=null) {
                            System.out.println("Response from Server: ");
                            System.out.println(response);
                            while ((response=in.readLine())!=null) {
                                System.out.println(response);
                            }
                        }
                    }
                } else {
                    throw new Exception("Invalid input!");
                }
            }
        } catch (UnknownHostException e) {
            System.err.println("Don't know about host " + hostName);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't get I/O for the connection to " +  hostName);
            System.exit(1);
        } catch (Exception e) {
            System.out.println(e);
        }
    }

}
