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
	List<Product> prList = new ArrayList<Product>();
	static String filePath = "productData/products.txt";

	public void saveProduct(Product p) {

		System.out.println(p + " in DAO");
		String data = p.getPid() + "," + p.getPname();
		FileUtil.writeProduct(data);
		System.out.println("Product Saved to File...");
	}

	public void showProduct() {
		FileUtil.readProducts();
	}

	public Product findProductById(int id) throws ProductNotFoundException {
		try {
			FileReader fr = new FileReader(filePath);
			BufferedReader br = new BufferedReader(fr);
			String line;

			while ((line = br.readLine()) != null) {
				String data[] = line.split(",");
				int pid = Integer.parseInt(data[0]);
				String pname = data[1];
				if (pid == id) {
					br.close();
					return new Product(pid, pname);
				}

			}
			br.close();
		} catch (NumberFormatException e) {

			e.printStackTrace();
		} catch (FileNotFoundException e) {

			e.printStackTrace();
		} catch (Exception e) {

			e.printStackTrace();
		}
		throw new ProductNotFoundException("Product with ID " + id + " not Found...");
	}

	public List<Product> getAllProducts() {
		try {
			FileReader fr = new FileReader(filePath);
			BufferedReader br = new BufferedReader(fr);
			String line;

			while ((line = br.readLine()) != null) {
				String data[] = line.split(",");
				int pid = Integer.parseInt(data[0]);
				String pname = data[1];

				prList.add(new Product(pid, pname));

			}
		} catch (NumberFormatException | IOException e) {

			e.printStackTrace();
		}
		return prList;
	}
}
