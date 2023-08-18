select distinct
       "MatchedObjectId" as matched_object_id,
       "PositionID" as position_id,
       "PositionTitle" as position_title,
       "PositionURI" as position_uri,
       "ApplyURI" as apply_uri,
       "PositionLocationDisplay" as position_location_display,
       "OrganizationName" as organization_name,
       "DepartmentName" as department_name,
       "MinimumRange"::float as minimum_range,
       "MaximumRange"::float as maximum_range,
       "RateIntervalCode" as rate_interval_code,
       "Description" as description,
       left("PositionStartDate",10)::date as position_start_date,
       left("PositionEndDate",10)::date as position_end_date,
       left("PublicationStartDate",10)::date as publication_start_date,
       left("ApplicationCloseDate",10)::date as application_close_date
from {{ source('src', 'job_postings') }}