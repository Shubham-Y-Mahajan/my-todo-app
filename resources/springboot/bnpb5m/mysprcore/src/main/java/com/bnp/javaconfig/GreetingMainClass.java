package com.bnp.javaconfig;

import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class GreetingMainClass {

	public static void main(String[] args) {
		ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);

		GreetingService gs11 = (GreetingService) context.getBean("gs1");

		GreetingService gs12 = (GreetingService) context.getBean("gs1");
		GreetingService gs13 = (GreetingService) context.getBean("gs1");
		// gs11.sayHello();

		System.out.println(gs11.hashCode());
		System.out.println(gs12.hashCode());
		System.out.println(gs13.hashCode());

	}

}
