package com.bnp.service;

import org.springframework.stereotype.Service;

@Service
public class FestivalDiscount implements DiscountService {

	@Override
	public void applyDiscount() {
		System.out.println("Festival Discount applied : 25%");

	}

}
