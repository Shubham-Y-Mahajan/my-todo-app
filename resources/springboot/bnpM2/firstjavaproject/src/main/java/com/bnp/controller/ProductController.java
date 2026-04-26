package com.bnp.controller;

import java.util.List;
import java.util.Scanner;

import com.bnp.dao.ProductDao;
import com.bnp.exception.ProductNotFoundException;
import com.bnp.model.Product;

public class ProductController {

	Product pr;
	Scanner sc = new Scanner(System.in);
	ProductDao dao = new ProductDao();

	public void addProduct(Product pr) {
		this.pr = pr;
		dao.saveProduct(pr);
		System.out.println("Product Added...");
	}

	public void showProduct() {
		// System.out.println(pr.getPid() + " -- " + pr.getPname());
		dao.viewProducts();
	}

	public Product searchProduct(int id) throws ProductNotFoundException {
		return dao.findProductById(id);
	}

	public List<Product> getAllProducts() {
		return dao.getAllProducts();

	}

}
