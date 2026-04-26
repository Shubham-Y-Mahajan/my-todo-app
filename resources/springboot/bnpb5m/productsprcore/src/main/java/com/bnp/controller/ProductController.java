package com.bnp.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;

import com.bnp.entity.Product;
import com.bnp.service.ProductService;

@Controller
public class ProductController {

	@Autowired
	private ProductService productService;
	
	public void displayProduct() {
		
		Product product  = productService.fetchProduct();
		System.out.println(product);
	}
	
	
}
