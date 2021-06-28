package com.wv.app;

import java.sql.Connection;
import java.sql.SQLException;
import org.apache.commons.dbcp2.BasicDataSource;





public class DBCPDataSource {
    
    private static final BasicDataSource ds = new BasicDataSource();
    
	
	
	
	
	
    static {
        ds.setUrl("jdbc:postgresql://XXXXXX");
        ds.setUsername("postgres");
        ds.setPassword("");
        ds.setMinIdle(10);
        ds.setMaxIdle(50);
        ds.setMaxOpenPreparedStatements(100);
    }
	
	
	
	
	
    
    public static Connection getConnection() throws SQLException {
        return ds.getConnection();
    }
	
	
	
	
	
	
    
    private DBCPDataSource(){}
		
		
		
}