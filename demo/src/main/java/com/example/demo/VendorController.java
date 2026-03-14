package com.example.demo;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/vendors")
@CrossOrigin(origins = "*") // Fixes CORS for Vercel!
public class VendorController {

    @Autowired
    private VendorRepository vendorRepository;

    @GetMapping("/")
    public List<Vendor> getAllVendors() {
        return vendorRepository.findAll();
    }

    @PostMapping("/")
    public Vendor createVendor(@RequestBody Vendor vendor) {
        return vendorRepository.save(vendor);
    }
}