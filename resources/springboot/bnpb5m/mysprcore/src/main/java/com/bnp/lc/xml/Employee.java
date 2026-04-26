package com.bnp.lc.xml;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.InitializingBean;

//public class Employee implements InitializingBean, DisposableBean {
public class Employee {
	private int id;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	@PostConstruct
	public void hi() {
		System.out.println("HI from Empl");
	}
	
	@PreDestroy
	public void bye() {
		System.out.println("Bye from empl");
	}
	
//	@Override
//	public void afterPropertiesSet() throws Exception {
//		System.out.println("After Properties set() called");
//
//	}
//
//	@Override
//	public void destroy() throws Exception {
//		System.out.println("Destroy() called");
//
//	}

}
