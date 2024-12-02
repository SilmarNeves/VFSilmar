
ALTER TABLE proventos 
ALTER COLUMN data_com TYPE DATE USING data_com::DATE,
ALTER COLUMN data_pagamento TYPE DATE USING data_pagamento::DATE;
