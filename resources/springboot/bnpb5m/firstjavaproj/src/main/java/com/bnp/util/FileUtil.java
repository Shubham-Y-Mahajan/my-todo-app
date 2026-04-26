package com.bnp.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class FileUtil {
	
	static String dirPath = "productData";
	static String filePath = dirPath +"/products.txt";
	
	public static void writeProduct(String data) {
		
		try {
			File dir = new File(dirPath);
			
			if(!dir.exists()) {
				dir.mkdir();
			}
			
			FileWriter fw = new FileWriter(filePath,true);
			BufferedWriter bw = new BufferedWriter(fw);
			bw.write(data);
			bw.newLine();
			
			bw.close();
		} catch (IOException e) {
			
			e.printStackTrace();
		}
		
	}
	
	public static void readProducts() {
		
		try {
			FileReader fr = new FileReader(filePath);
			BufferedReader br = new BufferedReader(fr);
			String line;
			
			while((line =br.readLine()) != null)
			{
				String data[] = line .split(",");
				int pid =Integer.parseInt(data[0]);
				String pname = data[1];
				
				System.out.println("Product ID : " + pid + " -- " + "Product Name :" + pname);
			}
		} catch (NumberFormatException e) {
			
			e.printStackTrace();
		} catch (FileNotFoundException e) {
			
			e.printStackTrace();
		} catch (IOException e) {
			
			e.printStackTrace();
		}finally {
			System.out.println("File Read operation successfully done...");
		}
	
		
	}

}






