CREATE OR REPLACE FUNCTION
improveSomeRatingsFunction(theParty TEXT, maxRatingImprovements INTEGER)
RETURNS INTEGER AS $$


    DECLARE
        numImproved INTEGER;
        theCandidateID INTEGER;
        theElectionDate INTEGER;
        theOfficeId INTEGER;
        theRating CHAR(1);
        
    DECLARE improvementCursor CURSOR FOR 
        SELECT o.candidateId, o.electionDate, o.officeId, o.rating
        FROM OfficeHolders o, CandidateForOffice cfo
        WHERE o.candidateID = cfo.candidateID
            AND o.electonDate = cfo.electionDate
            AND o.officeID = cfo.officeID
            AND cfo.party = theParty
            AND o.rating IN ('B','C','D','F')
        ORDER BY cfo.electionDate DESC;
        
    BEGIN
    -- Input Validation
    IF numImproved <= 0 THEN 
        RETURN -1;
    END IF;
    
        numImproved := 0;
        
        OPEN improvementCursor;
        
        LOOP
            
            FETCH improvementCursor INTO theCandidateId, theElectionDate, theOfficeId, theRating;
            
            EXIT WHEN NOT FOUND OR numImproved >= maxRatingImprovements;
            
            case theRating 
            
        WHEN 'B' THEN 
            UPDATE OfficeHolders
            SET rating = 'A'
            WHERE candidateID = theCandidateID 
                AND electionDate = theElectionDate
                AND officeID = theOfficeID;
                
            numImproved := numImproved + 1; 
            
        WHEN 'C' THEN 
            UPDATE OfficeHolders 
            SET rating = 'B'
            WHERE candidateID = theCandidateID 
                AND electionDate = theElectionDate 
                AND officeID = theOfficeID;
                
            numImproved := numImproved + 1;
            
        WHEN 'D' THEN 
            UPDATE OfficeHolders 
            SET rating 'C'
            WHERE candidateID = theCandidateID 
                AND electionDate = theElectionDate 
                AND officeID = theOfficeID 
                
            numImproved := numImproved + 1
            
        WHEN 'F' THEN 
            UPDATE OfficeHolders 
            SET rating = 'D'
            WHERE candidateID = theCnadidateID 
                AND electionDate = theElectionDate
                AND officeID = theOfficeID;
                
            numImproved := numImproved + 1;
            
        END CASE;
        
        END LOOP;
        
        CLOSE improvementCursor;
        
        RETURN numImproved;
    
    END;
    
$$ LANGUAGE plpgsql;
    
    
    