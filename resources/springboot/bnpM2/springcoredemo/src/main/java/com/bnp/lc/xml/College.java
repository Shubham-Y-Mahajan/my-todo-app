package com.bnp.lc.xml;

import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.InitializingBean;

public class College {
	private int id;

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	@Override
	public String toString() {
		return "College [id=" + id + "]";
	}

	@PostConstruct
	public void hi() {
		System.out.println("hi hi hi");
	}
	
	@PreDestroy
	public void bye() {
		System.out.println("Bye bye bye");
	}

}
