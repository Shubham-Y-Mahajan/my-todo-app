package com.bnp.view;

import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

import com.bnp.controller.ProductController;
import com.bnp.exception.ProductNotFoundException;
import com.bnp.functional.ProductOperation;
import com.bnp.model.Product;

public class MainClass {

	public static void main(String[] args) {
		ProductController pc = new ProductController();
		Scanner sc = new Scanner(System.in);
		String continueChoice = null;
		do {
			System.out.println("1. Add Product");
			System.out.println("2.View Product");
			System.out.println("3. Find Product  by id");
			System.out.println("4. Get All Products");
			System.out.println("Enter Choice:");
			int choice = sc.nextInt();
			switch (choice) {
			case 1: {

				System.out.println("Enter id");
				int id = sc.nextInt();

				System.out.println("Enter name");
				String name = sc.next();

				Product p = new Product(id, name);
				// p.setPid(id);
				// p.setPname(name);
				pc.addProduct(p);
				break;
			}

			case 2: {

				pc.viewProduct();

				break;
			}

			case 3: {

				System.out.println("Enter id");
				int id = sc.nextInt();

				try {
					Product product = pc.findProductById(id);
					System.out.println(
							"Product ID : " + product.getPid() + " -- " + "Product Name :" + product.getPname());
				} catch (ProductNotFoundException e) {

					e.printStackTrace();
				}

				break;
			}

			case 4: {

				List<Product> prList = pc.getAllProducts();
				
//				Iterator<Product> it  = prList.iterator();
//				while(it.hasNext()) {
//					System.out.println(it.next());
//				}
				
				ProductOperation  ops=(prod) -> {
					System.out.println(prod.getPid()+ " *** "  + prod.getPname());
				};
				
				ops.printHeader();
				//prList.forEach(pr -> System.out.println(pr));
				prList.forEach(ops::perform);
				ProductOperation.printFooter();
				break;
			}
			default: {
				break;
			}

			}
			System.out.println("Do u wanna continue? Y | y");
			continueChoice = sc.next();
		} while (continueChoice.equals("Y") || continueChoice.equals("y"));
		System.out.println("Thanks for using our system...");
	}
}
