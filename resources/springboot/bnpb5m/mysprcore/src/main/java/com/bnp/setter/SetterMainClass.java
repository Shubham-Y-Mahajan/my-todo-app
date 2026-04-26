package com.bnp.setter;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;


public class SetterMainClass {

	public static void main(String[] args) {
		ApplicationContext context = new ClassPathXmlApplicationContext("setter.xml");
//		Car  car = (Car)context.getBean("car");
//		System.out.println(car.getName() + " -- " + car.getModel());
//		
		User  user = (User)context.getBean("user");
		System.out.println(user.getUserName()+ " has a " +  user.getCar().getName() + " - " + user.getCar().getModel());
	}

}
