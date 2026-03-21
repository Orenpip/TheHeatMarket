-- CreateEnum
CREATE TYPE "public"."OpportunityCategory" AS ENUM ('COMPETITION', 'RESEARCH', 'EVENT', 'HACKATHON', 'PROGRAM', 'CLUB', 'VOLUNTEER', 'PUBLICATION');

-- CreateEnum
CREATE TYPE "public"."OpportunityScope" AS ENUM ('GLOBAL', 'SCHOOL');

-- CreateEnum
CREATE TYPE "public"."OpportunityStatus" AS ENUM ('DRAFT', 'PUBLISHED', 'ARCHIVED');

-- CreateTable
CREATE TABLE "Opportunity" (
    "id" TEXT NOT NULL,
    "scope" "OpportunityScope" NOT NULL DEFAULT 'SCHOOL',
    "status" "OpportunityStatus" NOT NULL DEFAULT 'DRAFT',
    "category" "OpportunityCategory" NOT NULL,
    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "url" TEXT,
    "location" TEXT,
    "organizerName" TEXT,
    "gradeLevels" INTEGER[] DEFAULT ARRAY[9, 10, 11, 12]::integer[],
    "deadline" TIMESTAMP(3),
    "startDate" TIMESTAMP(3),
    "endDate" TIMESTAMP(3),
    "tags" TEXT[] DEFAULT ARRAY[]::text[],
    "metadata" JSONB NOT NULL DEFAULT '{}',
    "schoolId" TEXT,
    "counselorId" TEXT,
    "embeddedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Opportunity_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "StudentOpportunityInteraction" (
    "id" TEXT NOT NULL,
    "studentId" TEXT NOT NULL,
    "opportunityId" TEXT NOT NULL,
    "viewedAt" TIMESTAMP(3),
    "savedAt" TIMESTAMP(3),
    "clickedAt" TIMESTAMP(3),
    "dismissedAt" TIMESTAMP(3),
    "appliedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "StudentOpportunityInteraction_pkey" PRIMARY KEY ("id")
);

-- Add embedding column (vector type, separate from standard DDL)
ALTER TABLE "Opportunity" ADD COLUMN "embedding" vector(1024);

-- CreateIndex
CREATE INDEX "Opportunity_scope_status_idx" ON "Opportunity"("scope", "status");

-- CreateIndex
CREATE INDEX "Opportunity_schoolId_status_idx" ON "Opportunity"("schoolId", "status");

-- CreateIndex
CREATE INDEX "Opportunity_deadline_idx" ON "Opportunity"("deadline");

-- CreateIndex
CREATE INDEX "Opportunity_category_idx" ON "Opportunity"("category");

-- CreateUniqueIndex
CREATE UNIQUE INDEX "StudentOpportunityInteraction_studentId_opportunityId_key" ON "StudentOpportunityInteraction"("studentId", "opportunityId");

-- AddForeignKey
ALTER TABLE "Opportunity" ADD CONSTRAINT "Opportunity_schoolId_fkey" FOREIGN KEY ("schoolId") REFERENCES "School"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Opportunity" ADD CONSTRAINT "Opportunity_counselorId_fkey" FOREIGN KEY ("counselorId") REFERENCES "Counselor"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StudentOpportunityInteraction" ADD CONSTRAINT "StudentOpportunityInteraction_studentId_fkey" FOREIGN KEY ("studentId") REFERENCES "Student"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "StudentOpportunityInteraction" ADD CONSTRAINT "StudentOpportunityInteraction_opportunityId_fkey" FOREIGN KEY ("opportunityId") REFERENCES "Opportunity"("id") ON DELETE CASCADE ON UPDATE CASCADE;
