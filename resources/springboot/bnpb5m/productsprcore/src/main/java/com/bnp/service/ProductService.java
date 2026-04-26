package com.bnp.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;

import com.bnp.entity.Product;
import com.bnp.repository.ProductRepository;

@Service
public class ProductService {
	
		@Autowired
		private ProductRepository productRepository;
		
		@Autowired
		@Qualifier("regularDiscount")
		@Lazy
		private DiscountService  discountService;
		
		public Product fetchProduct() {
			
			Product product = productRepository.getProduct();
			discountService.applyDiscount();
			return product;
		}
}
