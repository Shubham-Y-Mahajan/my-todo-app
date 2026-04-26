package com.bnp.lc.xml;


import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;



public class LCMainClass {

	public static void main(String[] args) {
		AbstractApplicationContext context = new ClassPathXmlApplicationContext("spr-lc-xml.xml");
		Employee empl = (Employee)context.getBean("emp");
		System.out.println(empl.getId());
		
		context.registerShutdownHook();

	}

}
