package simplewebserver;

/****************************************************************
SimpleWebServer.java
This toy web server is used to illustrate security vulnerabilities. This web server only supports extremely simple HTTP GET requests.
****************************************************************/

import java.io.*;
import java.net.*;
import java.util.*;

public class SimpleWebServer {

    /* Run the HTTP server on this TCP port. */
    private static final int PORT = 8080;

    /* The socket used to process incoming connections from web clients */
    private static ServerSocket dServerSocket;

    public SimpleWebServer () throws Exception {
    	dServerSocket = new ServerSocket (PORT);
    }

    public void run() throws Exception {
    	while (true) {
    		/* wait for a connection from a client */
    		Socket s = dServerSocket.accept();

    		/* then process the client's request */
			try {
				processRequest(s);	
			} catch (Exception e) {
				//TODO: handle exception
				System.out.println(e);
			}
    	}
    }

	public void storeFile (BufferedReader br, OutputStreamWriter osw, String pathname) throws Exception {
		// extracts the file name to write it into the inbox/ directory
		pathname = "inbox/" + pathname.split("/")[pathname.split("/").length-1];
		BufferedWriter bw = new BufferedWriter(new FileWriter(new File(pathname)));
		
		// logs request entry to the access.log file 
		logEntry("access.log", "PUT" + "; " + pathname);
		
		/* read the HTTP request from the client 
		   and store it on the server */
		String response = br.readLine();
		if (response!=null) {
			bw.write(response);
			while ((response=br.readLine())!=null) {
				bw.write("\n"+response);
			}
		}
		bw.close();
	}

	public void logEntry (String filename, String record) throws IOException {
		BufferedWriter bw = new BufferedWriter(new FileWriter(new File(filename), true));
		bw.write(record+"\n");
		bw.close();
	}

    /* Reads the HTTP request from the client, and responds with the file the user requested or a HTTP error code. */
    public void processRequest(Socket s) throws Exception {
    	/* used to read data from the client */
		InputStreamReader isr = new InputStreamReader(s.getInputStream());
    	BufferedReader br = new BufferedReader (isr);

    	/* used to write data to the client */
    	OutputStreamWriter osw =  new OutputStreamWriter (s.getOutputStream());

    	/* read the HTTP request from the client */
    	String request = br.readLine();

    	String command = null;
    	String pathname = null;

    	/* parse the HTTP request */
    	StringTokenizer st = new StringTokenizer (request, " ");

    	command = st.nextToken();
    	pathname = st.nextToken();

    	if (command.equals("GET")) {
    		/* if the request is a GET try to respond with the file the user is requesting */
    		System.out.println("Request: " + "GET");
    		System.out.println("Path name: " + pathname);
    		serveFile(osw, pathname);
			osw.close();
    	} else if (command.equals("PUT")) {
			/* if the request is a PUT try to respond with the process status after saving file */
    		System.out.println("Request: " + "PUT");
			System.out.println("Path name: " + pathname);
			storeFile(br, osw, pathname);
			osw.close();
		} else {
    		/* if the request is a NOT a GET, return an error saying this server does not implement the requested command */
    		osw.write ("HTTP/1.0 501 Not Implemented\n\n");
			osw.close();
    	}

    	/* close the connection to the client */
    	osw.close();
    }

    public void serveFile (OutputStreamWriter osw, String pathname) throws Exception {
    	FileReader fr=null;
    	int c=-1;
    	StringBuffer sb = new StringBuffer();
    	/* remove the initial slash at the beginning of the pathname in the request */
    	if (pathname.charAt(0)=='/')
    		pathname=pathname.substring(1);

    	/* if there was no filename specified by the client, serve the "index.html" file */
    	if (pathname.equals(""))
    		pathname="index.html";

    	/* try to open file specified by pathname */
    	try {
		//  System.out.println("Path name: "+pathname);
    		fr = new FileReader (pathname);
    		c = fr.read();
    	}
    	catch (Exception e) {
    		/* if the file is not found,return the appropriate HTTP response code  */
    		osw.write ("HTTP/1.0 404 Not Found\n\n");
    		fr.close();
			return;
    	}
		long maximumAllowedSize = 1024 * 1024; // 1 MB
		long fsize = new File(pathname).length();
		if (fsize >= maximumAllowedSize) {
			logEntry("error_log.txt", "File access tried; " + pathname + ": " + fsize + "." );
			osw.write ("HTTP/1.0 403 Forbidden\n\n");
		} else {
			/* if the requested file can be successfully opened
 	   		and read, then return an OK response code and
 	   		send the contents of the file */
				osw.write ("HTTP/1.0 200 OK\n\n");
				while (c != -1) {
					sb.append((char)c);
					c = fr.read();
				}
				osw.write (sb.toString());
		}
    }

    /* This method is called when the program is run from the command line. */
    public static void main (String argv[]) throws Exception {
    	/* Create a SimpleWebServer object, and run it */
    	SimpleWebServer sws = new SimpleWebServer();
    	sws.run();
    }
}
