package com.bnp.model;

public class ElectronicProduct extends Product{
	private int warranty;

	
	public ElectronicProduct() {
		super();
		// TODO Auto-generated constructor stub
	}


	public ElectronicProduct(int pid, String pname, int warranty) {
		super(pid, pname);
		this.warranty = warranty;
	}

//	public ElectronicProduct(String pid, int pname) {
//		//super(pid, pname);
//		// TODO Auto-generated constructor stub
//	}
//
//	public ElectronicProduct(int warranty) {
//		super();
//		this.warranty = warranty;
//	}
//	public ElectronicProduct(String warranty) {
//		super();
//	
//	}
	@Override
	public String display() {
		return getPid()+ " -- "+getPname() + " -- " + warranty;
	}


	@Override
	public String toString() {
		return "ElectronicProduct [ Pid " + getPid() + " -- Pname:" + getPname() +" Warranty: " + warranty + "]";
	}
	
	
	
}
