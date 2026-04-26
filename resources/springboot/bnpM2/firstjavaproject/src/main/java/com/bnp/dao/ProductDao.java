package com.bnp.dao;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.bnp.exception.ProductNotFoundException;
import com.bnp.model.Product;
import com.bnp.util.FileUtil;

public class ProductDao {
	String filePath = "productData/products.txt";
	List<Product> plist = new ArrayList<Product>();
	public void saveProduct(Product pr) {
		String data  = pr.getPid() + "," +pr.getPname();
		FileUtil.writeProduct(data);
		System.out.println("Product Saved Successfully !!!");
	}
	
	public void viewProducts() {
		FileUtil.readProducts();
	}
	
	public Product findProductById(int id) throws ProductNotFoundException{
		
		try {
			FileReader fr = new FileReader(filePath);
			BufferedReader br = new BufferedReader(fr);

			String line;

			while ((line = br.readLine()) != null) {
				String data[]=line.split(",");
				int pid=Integer.parseInt(data[0]);
				String pname = data[1];
				
				if(pid == id) {
					br.close();
					return new Product(pid, pname);
				}
			}

			br.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		throw new ProductNotFoundException("Product with ID " + id + " not found..");
		
	}
	
	public List<Product> getAllProducts(){
		try {
			FileReader fr = new FileReader(filePath);
			BufferedReader br = new BufferedReader(fr);

			String line;

			while ((line = br.readLine()) != null) {
				String data[]=line.split(",");
				int pid=Integer.parseInt(data[0]);
				String pname = data[1];
				plist.add(new Product(pid,pname));
			}

			br.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return plist;
	}
	
}
