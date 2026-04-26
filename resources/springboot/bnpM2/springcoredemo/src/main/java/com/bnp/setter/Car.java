package com.bnp.setter;

import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

@Component
public class Car {

	@Value("Honda")
	private String name;
	
	@Value("City 2")
	private String model;
	

	public Car() {
		super();
		// TODO Auto-generated constructor stub
	}

	
	public Car(String name, String model) {
		
		super();
		this.name = name;
		this.model = model;
		System.out.println("From Car Constructr  -" + name + " -- " + model);
	}


	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getModel() {
		return model;
	}

	public void setModel(String model) {
		this.model = model;
	}

	@Override
	public String toString() {
		return "Car [name=" + name + ", model=" + model + "]";
	}

}
