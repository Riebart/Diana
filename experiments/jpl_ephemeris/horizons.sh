#!/bin/bash

#http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND='499'&MAKE_EPHEM='YES'  
#  &TABLE_TYPE='OBSERVER'&START_TIME='2000-01-01'&STOP_TIME='2000-12-31'&STEP_SIZE='15%20d'  
#  &QUANTITIES='1,9,20,23,24'&CSV_FORMAT='YES'  

bodies="10 Sun
199 Mercury
299 Venus
301 Moon
399 Earth
401 Phobos
402 Deimos
499 Mars
501 Io
502 Europa
503 Ganymede
504 Callisto
505 Amalthea
506 Himalia
507 Elara
508 Pasiphae
509 Sinope
510 Lysithea
511 Carme
512 Ananke
513 Leda
514 Thebe
515 Adrastea
516 Metis
517 Callirrhoe
518 Themisto
519 Megaclite
520 Taygete
521 Chaldene
522 Harpalyke
523 Kalyke
524 Iocaste
525 Erinome
526 Isonoe
527 Praxidike
528 Autonoe
529 Thyone
530 Hermippe
531 Aitne
532 Eurydome
533 Euanthe
534 Euporie
535 Orthosie
536 Sponde
537 Kale
538 Pasithee
539 Hegemone
540 Mneme
541 Aoede
542 Thelxinoe
543 Arche
544 Kallichore
545 Helike
546 Carpo
547 Eukelade
548 Cyllene
549 Kore
550 Herse
551 2010J1
552 2010J2
553 Dia
599 Jupiter
601 Mimas
602 Enceladus
603 Tethys
604 Dione
605 Rhea
606 Titan
607 Hyperion
608 Iapetus
609 Phoebe
610 Janus
611 Epimetheus
612 Helene
613 Telesto
614 Calypso
615 Atlas
616 Prometheus
617 Pandora
618 Pan
619 Ymir
620 Paaliaq
621 Tarvos
622 Ijiraq
623 Suttungr
624 Kiviuq
625 Mundilfari
626 Albiorix
627 Skathi
628 Erriapus
629 Siarnaq
630 Thrymr
631 Narvi
632 Methone
633 Pallene
634 Polydeuces
635 Daphnis
636 Aegir
637 Bebhionn
638 Bergelmir
639 Bestla
640 Farbauti
641 Fenrir
642 Fornjot
643 Hati
644 Hyrrokkin
645 Kari
646 Loge
647 Skoll
648 Surtur
649 Anthe
650 Jarnsaxa
651 Greip
652 Tarqeq
653 Aegaeon
699 Saturn
701 Ariel
702 Umbriel
703 Titania
704 Oberon
705 Miranda
706 Cordelia
707 Ophelia
708 Bianca
709 Cressida
710 Desdemona
711 Juliet
712 Portia
713 Rosalind
714 Belinda
715 Puck
716 Caliban
717 Sycorax
718 Prospero
719 Setebos
720 Stephano
721 Trinculo
722 Francisco
723 Margaret
724 Ferdinand
725 Perdita
726 Mab
727 Cupid
799 Uranus
801 Triton
802 Nereid
803 Naiad
804 Thalassa
805 Despina
806 Galatea
807 Larissa
808 Proteus
809 Halimede
810 Psamathe
811 Sao
812 Laomedeia
813 Neso
814 2004N1
899 Neptune
901 Charon
902 Nix
903 Hydra
904 Kerberos
905 Styx
999 Pluto"

echo "$bodies" | while read obj_id obj_name
do
base_url="http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&
COMMAND='$obj_id'&
CENTER='500@0'&
MAKE_EPHEM='YES'&
TABLE_TYPE='VECTORS'&
START_TIME='2015-12-31'&
STOP_TIME='2016-01-01'&
STEP_SIZE='1'&
OUT_UNITS='KM-S'&
VECT_TABLE='2'&
REF_PLANE='ECLIPTIC'&
REF_SYSTEM='J2000'&
VECT_CORR='NONE'&
VEC_LABELS='YES'&
CSV_FORMAT='YES'&
OBJ_DATA='YES'"

#jpl_data=$(echo $base_url | wget -qO- -i - | grep -A1 "\$\$SOE" | tail -n1)

jpl_data=$(echo $base_url | wget -qO- -i -)
radius=$(echo "$jpl_data" | grep -i "Radius")
mass=$(echo "$jpl_data" | grep -i "Mass")
spatial=$(echo "$jpl_data" | grep -A1 "\$\$SOE" | tail -n1)
echo "$obj_id,$obj_name,$radius"
echo "$obj_id,$obj_name,$mass"
echo "$obj_id,$obj_name,$spatial"
done
