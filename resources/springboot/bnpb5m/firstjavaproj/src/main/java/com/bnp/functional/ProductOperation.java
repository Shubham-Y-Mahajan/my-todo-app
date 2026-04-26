package com.bnp.functional;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.bnp.model.Product;

@FunctionalInterface
public interface ProductOperation {
	void perform(Product product);

	public default void printHeader() {
		System.out.println("**************");
	}

	public static void printFooter() {
		System.out.println("*******  End *******");
	}
}
/*
 * @FunctionalInterface interface Calculate { public void add(int a, int b);
 * 
 * 
 * }
 * 
 * /* public class ProductOperation {
 * 
 * 
 * public static void main(String[] args) { ProductOperation cl = new
 * ProductOperation();
 * 
 * Calculate c=(a, b) -> { System.out.println(a + b); }; c.printHeader();
 * c.add(12, 12); Calculate.printFooter();
 * 
 * 
 * List<String> strList = Arrays.asList("bat","cat","rat","lion","Tiger");
 * 
 * //long count = getCountStrwithLength3(strList); long count =
 * strList.stream().filter(str -> str.length() == 3).count();
 * System.out.println(count); }
 * 
 * /*private static long getCountStrwithLength3(List<String> strList) { long
 * count =0;
 * 
 * for(String str : strList) { if(str.length() == 3) { count++; } }
 * 
 * return count; }
 * 
 * }
 */
