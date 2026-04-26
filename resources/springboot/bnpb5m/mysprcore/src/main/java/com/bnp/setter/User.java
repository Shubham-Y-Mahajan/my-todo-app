package com.bnp.setter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Component;

@Component
public class User {
	@Value("Priyanshu")
	private String userName;
	
	@Autowired
	private Car car;

	public User() {
		super();
		// TODO Auto-generated constructor stub
	}

	public User(String userName, Car car) {
		super();
		this.userName = userName;
		this.car = car;
	}

	public String getUserName() {
		return userName;
	}

	public void setUserName(String userName) {
		this.userName = userName;
	}

	public Car getCar() {
		return car;
	}

	public void setCar(Car car) {
		this.car = car;
	}

	@Override
	public String toString() {
		return "User [userName=" + userName + ", car=" + car + "]";
	}

}
