package com.bnp;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import com.bnp.config.AppConfig;
import com.bnp.controller.ProductController;

public class MainApp {

	public static void main(String[] args) {
		AnnotationConfigApplicationContext  context = new AnnotationConfigApplicationContext();
		
		context.register(AppConfig.class);
		context.refresh();

		ProductController cont1 = context.getBean(ProductController.class);
		System.out.println(cont1.hashCode());
		
		
		
		
		ProductController cont2 = context.getBean(ProductController.class);
		System.out.println(cont2.hashCode());
		
		cont1.displayProduct();
		cont2.displayProduct();
		context.close();
		
	}

}
