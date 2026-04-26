package com.bnp.repository;

import org.springframework.stereotype.Repository;

import com.bnp.entity.Product;

@Repository
public class ProductRepository {

	public Product getProduct() {
		
		Product p = new Product();
		p.setPid(101);
		p.setPname("iphone");
		return p;
	}
	
}
