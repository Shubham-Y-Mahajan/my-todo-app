package com.bnp.controller;

import java.util.List;
import java.util.Scanner;

import com.bnp.dao.ProductDao;
import com.bnp.exception.ProductNotFoundException;
import com.bnp.model.Product;

public class ProductController {

	Product p ;
	ProductDao dao = new ProductDao();
	
	public void addProduct(Product p) {
		
		this.p = p;
		dao.saveProduct(p);
		
		System.out.println("Product Added Successfully !!!");
	}

	public void viewProduct() {
		//System.out.println(p.getPid() + p.getPname());
		dao.showProduct();
	}
	
	public Product findProductById(int id) throws ProductNotFoundException {
		
		return dao.findProductById(id);
	}
	
	public List<Product> getAllProducts() {
		
		return dao.getAllProducts();
	}
}








