
QUERY_NEGATIVE=(

"(existence:1) AND (length:[40 TO *]) AND (reviewed:true) AND (fragment:false) AND (taxonomy_id:2759) NOT (ft_signal:*) AND ((cc_scl_term_exp:SL-0091) OR (cc_scl_term_exp:SL-0191) OR (cc_scl_term_exp:SL-0173) OR (cc_scl_term_exp:SL-0204) OR (cc_scl_term_exp:SL-0209) OR (cc_scl_term_exp:SL-0039))" 
)
QUERY_POSITIVE = (
" (fragment:false) AND (reviewed:true) AND  (existence:1) AND (taxonomy_id:2759) AND (length:[40 TO *]) AND (NOT ft_signal_exp:*) "
)
OUTPUT_DIR = "uniprot_results"
