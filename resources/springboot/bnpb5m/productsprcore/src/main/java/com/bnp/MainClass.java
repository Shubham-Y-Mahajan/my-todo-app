package com.bnp;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import com.bnp.config.AppConfig;
import com.bnp.controller.ProductController;

public class MainClass {

	public static void main(String[] args) {
		
		AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
		context.register(AppConfig.class);
		context.refresh();
		
		ProductController controller = context.getBean(ProductController.class);
		controller.displayProduct();
		
		context.close();

	}

}
