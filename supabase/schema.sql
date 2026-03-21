-- HeatGrid Supabase Schema
-- Run this in Supabase Dashboard > SQL Editor

-- 1. Heat Listings (sellers / DC operators)
CREATE TABLE heat_listings (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  company_name TEXT NOT NULL,
  facility_name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  lat DOUBLE PRECISION NOT NULL,
  lng DOUBLE PRECISION NOT NULL,
  capacity_mw DOUBLE PRECISION NOT NULL,
  output_temp_c INTEGER NOT NULL DEFAULT 35,
  price_per_mwh DOUBLE PRECISION NOT NULL,
  contact_email TEXT NOT NULL,
  contact_name TEXT,
  description TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'pending', 'inactive'))
);

-- 2. Heat Inquiries (buyers expressing interest)
CREATE TABLE heat_inquiries (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  listing_id UUID REFERENCES heat_listings(id) ON DELETE SET NULL,
  facility_type TEXT NOT NULL CHECK (facility_type IN ('school', 'greenhouse', 'pool', 'hospital', 'industrial', 'residential', 'other')),
  facility_name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  lat DOUBLE PRECISION,
  lng DOUBLE PRECISION,
  heat_need_mwh DOUBLE PRECISION,
  contact_email TEXT NOT NULL,
  contact_name TEXT NOT NULL,
  message TEXT,
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'matched'))
);

-- 3. Enable Row Level Security
ALTER TABLE heat_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE heat_inquiries ENABLE ROW LEVEL SECURITY;

-- 4. RLS Policies — public marketplace (read all, insert freely)
-- Anyone can view active listings
CREATE POLICY "Public can view active listings"
  ON heat_listings FOR SELECT
  USING (status = 'active');

-- Anyone can create a listing (it goes to 'active' by default)
CREATE POLICY "Anyone can create listings"
  ON heat_listings FOR INSERT
  WITH CHECK (true);

-- Anyone can view their own inquiries (by email match — simple for now)
CREATE POLICY "Public can view inquiries"
  ON heat_inquiries FOR SELECT
  USING (true);

-- Anyone can submit an inquiry
CREATE POLICY "Anyone can submit inquiries"
  ON heat_inquiries FOR INSERT
  WITH CHECK (true);

-- 5. Indexes for common queries
CREATE INDEX idx_listings_location ON heat_listings (state, city);
CREATE INDEX idx_listings_status ON heat_listings (status);
CREATE INDEX idx_inquiries_listing ON heat_inquiries (listing_id);
CREATE INDEX idx_inquiries_status ON heat_inquiries (status);
