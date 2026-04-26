package com.bnp.repository;

import org.springframework.stereotype.Repository;

import com.bnp.model.Product;

@Repository
public class ProductRepository {
	public Product getProduct() {
		Product p = new Product();
		p.setPid(200);
		p.setPname("AC");
		return p;
	}
}
