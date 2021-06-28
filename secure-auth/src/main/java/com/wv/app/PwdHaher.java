package com.wv.app;

import java.nio.charset.Charset;
import java.security.NoSuchAlgorithmException;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.Arrays;
import java.util.Base64;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;


class PwdHasher {
	
	
	
    public final Integer DEFAULT_ITERATIONS = 19000;
    public final String algorithm = "pbkdf2-sha512";
    
    public PwdHasher() {}
		
		
		
		
		
		
    
    public String getEncodedHash(String password, String salt, int iterations) {
        // Returns only the last part of whole encoded password
        SecretKeyFactory keyFactory = null;

        try {
            keyFactory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA512");
        } catch (NoSuchAlgorithmException e) {
            System.err.println("Could NOT retrieve PBKDF2WithHmacSHA512 algorithm");
            System.exit(1);
        }
		
		
        KeySpec keySpec = new PBEKeySpec(password.toCharArray(), salt.getBytes(Charset.forName("UTF-8")), iterations, 512);
        SecretKey secret = null;
        try {
            secret = keyFactory.generateSecret(keySpec);
        } catch (InvalidKeySpecException e) {
            System.out.println("Could NOT generate secret key");
            e.printStackTrace();
        }
        
        byte[] rawHash = secret.getEncoded();
        byte[] hashBase64 = Base64.getEncoder().encode(rawHash);
        
        return new String(hashBase64);
    }
	
	
	
    
    public String encode(String password, String salt, int iterations) {
        // returns hashed password, along with algorithm, number of iterations and salt
		
		if(salt == null || salt.isEmpty()) {
			
			salt = "1234567812345678";
		}
		
        String hash = getEncodedHash(password, salt, iterations);
        return String.format("%s$%d$%s$%s", algorithm, iterations, salt, hash);
    }
	
	
	
	
	
	
	
    
    public String encode(String password, String salt) {
        return this.encode(password, salt, this.DEFAULT_ITERATIONS);
    }
	
	
	
	
	
	
	
	
    
    public boolean checkPassword(String password, String hashedPassword) {
        // hashedPassword consist of: ALGORITHM, ITERATIONS_NUMBER, SALT and
        // HASH; parts are joined with dollar character ("$")
        String[] parts = hashedPassword.split("\\$");
        if (parts.length != 4) {
            // wrong hash format
            return false;
        }
        Integer iterations = Integer.parseInt(parts[1]);
        String salt = parts[2];
        String hash = encode(password, salt, iterations);
        
        return hash.equals(hashedPassword);
    }
    
  
  
  
  
  
    
    private static void passwordShouldMatch(String password, String expectedHash) {
		
        PwdHasher hasher = new PwdHasher();
        
        if (hasher.checkPassword(password, expectedHash)) {
            System.out.println(" => OK");
        } else {
            String[] parts = expectedHash.split("\\$");
            if (parts.length != 4) {
                System.out.printf(" => Wrong hash provided: '%s'\n", expectedHash);
                return;
            }
            String salt = parts[2];
            String resultHash = hasher.encode(password, salt);
            String msg = " => Wrong! Password '%s' hash expected to be '%s' but is '%s'\n";
            System.out.printf(msg, password, expectedHash, resultHash);
        }
    }
	
	
	
	
	
	
	
	
    
    private static void passwordShouldNotMatch(String password, String expectedHash) {
        PwdHasher hasher = new PwdHasher();
        
        if (hasher.checkPassword(password, expectedHash)) {
            System.out.printf(" => Wrong (password '%s' did '%s' match but were not supposed to)\n", password, expectedHash);
        } else {
            System.out.println(" => OK (password didn't match)");
        }
    }
    
}
