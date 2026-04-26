package com.bnp.functional;

import com.bnp.model.Product;

@FunctionalInterface
public interface ProductOps {

	public void perform(Product product);
	
	public default void printHeader() {
		System.out.println("-------  Product Details --------");
	}
	public static void printFooter() {
		System.out.println("------- End of Product Details --------");
	}
}


/*
(product) -> {

    S.o.p(product.getPid()+ product.getPname());

}

*/