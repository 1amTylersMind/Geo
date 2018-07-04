import java.util.*;
import java.nio.file.*;
import java.io.*;
import java.io.File;

class TextFileReader implements Runnable {

	private File file;
    private final String [] modes = {"trace","geo"};
    private static int MODE;
    Map<String,Vector<String>> netinfo = new HashMap<>();
    Map<String,Vector<String>> geoinfo = new HashMap<>();
    
	TextFileReader(String mode, String fname){
		this.file = Paths.get(System.getProperty("user.dir"),fname).toFile();
		switch(mode){
			case "trace":
				TextFileReader.MODE = 0;
				break;
			case "geo":
				TextFileReader.MODE = 1;
				break;
			default:
				break;
		}
	}	
	
	public void run(){
		Vector<String> content = new Vector<>();
		try{content = parseContent(this.file);}
		catch(Exception e){e.printStackTrace();}
		if(TextFileReader.MODE==0){this.netinfo = interpretTraceFile(content);}
		if(TextFileReader.MODE==1){this.geoinfo = interpretGeoFile(content);}
	}
	
	Vector<String>  parseContent(File f) throws Exception{
		Vector<String> content = new Vector<>();
		BufferedReader br = null;
		br = new BufferedReader(new FileReader(f));
		String ln = null;
		while((ln = br.readLine()) != null){content.add(ln);}
		
		return content;
	}
	
	Map<String,Vector<String>> interpretTraceFile(Vector<String>data){
		Map<String,Vector<String>> struct = new HashMap<>();
		int index = 0;
		Vector<String> DNS = new Vector<>();
		Vector<String> IP = new Vector<>();
        // Run through the input traceroute text file line by line 
		for(String line : data){
			try{
			if(!line.contains(" * ")){DNS.add(line.split("\\(")[0].split("\\d\\s ")[1]);}
			IP.add(line.split("\\(")[1].split("\\)")[0]);}//DNS
		    catch(ArrayIndexOutOfBoundsException e){}
		}
		IP.remove(0); 
		//System.out.println("DNS' encountered");
		//for(String dns : DNS){System.out.println(dns);}
		//System.out.println("IP Trace:");
		for(String ip : IP){System.out.println(ip);}
		struct.put("IP",IP);
		struct.put("DNS",DNS);
		return struct;
	}
	
	Map<String,Vector<String>> interpretGeoFile(Vector<String>data){
	    Map<String,Vector<String>> struct = new HashMap<>();
        Vector<String> ip_list = new Vector<>();
		Vector<String> cities = new Vector<>();
		Vector<String> region = new Vector<>();
		Vector<String> geoloc = new Vector<>();
		for(String ln : data){
		    if(ln.contains("ip")){ip_list.add(ln.split(":")[1]);}  
		    if(ln.contains("city")){cities.add(ln.split(":")[1]);}
		    if(ln.contains("region")){region.add(ln.split(":")[1]);}
		    if(ln.contains("loc")){geoloc.add(ln.split(":")[1]);}
		}
		if(ip_list.size()==cities.size() && cities.size()==region.size() 
		    && ip_list.size()==geoloc.size()){
		    int index = 0;
		    for(String ip : ip_list){
		        Vector<String> geoLocationData = new Vector<>();
		        geoLocationData.add(cities.get(index));
		        geoLocationData.add(region.get(index));
		        geoLocationData.add(geoloc.get(index));
		        struct.put(ip,geoLocationData);
		        index += 1;
		    }
		 }
		 /** <Display GeoLocation Information >*/
		for(Map.Entry<String,Vector<String>> entry: struct.entrySet()){
		    String row = "* ";
		    row += entry.getKey() + " : ";
		    for(String s : entry.getValue()){row+=s + " ";}
		    System.out.println(row);
		}
		return struct;
	}
	
	
	static void usage(){
		System.out.println("****************************************");
		System.out.println("* Incorrect Usage or Bad Args. Ex:     *");
		System.out.println("* java TextFileReader -mode -file.ext  *");
		System.out.println("****************************************");
	}
	

	public static void main(String[]args){
		if(args.length<2){usage();}
		else{
			TextFileReader tfr;
			switch(args[0]){
				case "-trace":
					tfr = new TextFileReader("trace",args[1]);
					tfr.run();
					break;
					
				case "-geo":
					tfr= new TextFileReader("geo",args[1]);
					tfr.run();
					break;
					
				default:
					System.out.println("Unrecognized Argument...");usage();
					break;
			}
			
		}
		
	}

}
/** TextFileReader.java **/