package com.bnp.lc.xml;

import org.springframework.context.ApplicationContext;
import org.springframework.context.support.AbstractApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class LcXmlMainClass {

	public static void main(String[] args) {
		AbstractApplicationContext context  = new ClassPathXmlApplicationContext("spr-lc-xml.xml");
		
		College c = (College)context.getBean("college");
		System.out.println(c.getId());
		
		context.registerShutdownHook();
	}

}
