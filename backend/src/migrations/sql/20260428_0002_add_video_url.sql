-- Migration: Add video_url column to generated_clips table
-- Description: Supports external storage (S3/R2) for generated clips.

ALTER TABLE generated_clips ADD COLUMN IF NOT EXISTS video_url VARCHAR(1000);
