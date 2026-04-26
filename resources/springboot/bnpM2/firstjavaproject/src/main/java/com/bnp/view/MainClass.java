package com.bnp.view;

import java.util.Iterator;
import java.util.List;
import java.util.Scanner;

import com.bnp.controller.ProductController;
import com.bnp.exception.ProductNotFoundException;
import com.bnp.functional.ProductOps;
import com.bnp.model.ElectronicProduct;
import com.bnp.model.Product;

public class MainClass {

	public static void main(String[] args) {

		ProductController pc = new ProductController();
		Scanner sc = new Scanner(System.in);

		String continueChoice = null;
		do {
			System.out.println("1. Add Product");
			System.out.println("2. Show Product");
			System.out.println("3. Add Electronic Product");
			System.out.println("4. Search Product by ID");
			System.out.println("5. Get All Products using Lambda");

			System.out.println("Enter your choice");
			int choice = sc.nextInt();
			switch (choice) {

			case 1: {
				System.out.println("Enter product ID:");
				int pid = sc.nextInt();
				// pr.setPid(pid);

				System.out.println("Enter Product Name:");
				String pname = sc.next();
				// pr.setPname(pname);

				Product p = new Product(pid, pname);

				pc.addProduct(p);
				break;
			}

			case 2: {
				pc.showProduct();
				break;
			}

			case 3: {
				System.out.println("Enter product ID:");
				int pid = sc.nextInt();
				// pr.setPid(pid);

				System.out.println("Enter Product Name:");
				String pname = sc.next();

				System.out.println("Enter Product Warranty:");
				int waranty = sc.nextInt();

				Product ep = new ElectronicProduct(pid, pname, waranty);
				pc.addProduct(ep);
				break;
			}

			case 4: {
				System.out.println("Enter product ID:");
				int pid = sc.nextInt();

				try {
					Product product = pc.searchProduct(pid);
					System.out.println(product.getPid() + " -- " + product.getPname());
				} catch (ProductNotFoundException e) {
					System.out.println(e.getMessage());
					// e.printStackTrace();
				}
				break;
			}

			case 5: {
				List<Product> prList = pc.getAllProducts();
//			Iterator<Product> it = prList.iterator();
//			while(it.hasNext()) {
//				System.out.println(it.next());
//			}

				ProductOps ops = (product) -> {
					System.out.println(product.getPid() + product.getPname());
				};
				
				ops.printHeader();
				prList.forEach(ops::perform);
				
				ProductOps.printFooter();							
				break;
			}
			default: {
				System.out.println("Choose the right choice");
			}
			}
			System.out.println("Do u wanna continue? Y / y");
			continueChoice = sc.next();
		} while (continueChoice.equals("Y") || continueChoice.equals("y"));

	}

}

/*
 * object -- place holder / ref variable instance -- reference // memeory
 * address
 * 
 */
