select distinct
       "MatchedObjectId" as matched_object_id,
       "PromotionPotential" as promotion_potential,
       COALESCE("SubAgencyName" ,'NA') as subagency_name,
       "Relocation" as relocation,
       COALESCE("TotalOpenings", 'NA') as total_openings,
       "TravelCode" as travel_code,
       COALESCE("AgencyContactEmail",'NA') as agency_contact_email,
       "SecurityClearance" as security_clearance,
       "RemoteIndicator" as remote_indicator
       from {{ source('src', 'user_area') }}