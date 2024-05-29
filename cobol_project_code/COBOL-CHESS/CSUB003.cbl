      ******************************************************************
      * Author:
      * Date:
      * Purpose:
      * Tectonics: cobc
      ******************************************************************
       IDENTIFICATION DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       PROGRAM-ID. CSUB003.
       ENVIRONMENT DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       CONFIGURATION SECTION.
      *-----------------------
       INPUT-OUTPUT SECTION.

       FILE-CONTROL.
           SELECT INFILE ASSIGN TO
           "C:\Users\xxbystea\CHESS_SAVE.txt"
           ORGANIZATION IS LINE SEQUENTIAL
           .
      *-----------------------
       DATA DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       FILE SECTION.
       FD INFILE.
       01 MY-RECORD PIC X(200).
      *-----------------------
       WORKING-STORAGE SECTION.
       01 COUNTERS.
           05 COUNTER          PIC 99.
           05 COUNTER2         PIC 99.
       01 SWITCHES.
           05 SWITCH-EOF       PIC X.
               88 EOF-Y        VALUE 'Y'.
               88 NOT-EOF      VALUE 'N'.
      *INPUT AREA
       01 I-INPUT-AREA.
           05 I-INPUT OCCURS 32 TIMES.
               10 IN-ID        PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-X         PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-Y         PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-NAME      PIC XX.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-FIRST     PIC X.


       LINKAGE SECTION.
       01 PLAYER-TURN          PIC X(1).
               88 W-TURN       VALUE 'W'.
               88 B-TURN       VALUE 'B'.
           COPY COORDINATES.
      *-----------------------
       PROCEDURE DIVISION USING COORDINATES
                                PLAYER-TURN.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       MAIN-PROCEDURE.

           PERFORM A-WRITE-FILE
           DISPLAY "THE GAME WAS SAVED!"
           GOBACK
           .


           A-WRITE-FILE SECTION.

      *******************************************************************
      *                        A-WRITE-FILE SECTION                     *
      *******************************************************************

           OPEN OUTPUT INFILE
           MOVE 1 TO COUNTER2
           WRITE MY-RECORD FROM PLAYER-TURN
           PERFORM UNTIL COUNTER2 > 16
               MOVE COUNTER2 TO IN-ID(COUNTER2)
               MOVE W-X-VAR(COUNTER2) TO IN-X(COUNTER2)
               MOVE W-Y-POS(COUNTER2) TO IN-Y(COUNTER2)
               MOVE W-PIECE(COUNTER2) TO IN-NAME(COUNTER2)
               MOVE W-FIRST(COUNTER2) TO IN-FIRST(COUNTER2)

               WRITE MY-RECORD FROM I-INPUT(COUNTER2)
               ADD 1 TO COUNTER2

           END-PERFORM
           MOVE 1 TO COUNTER2
           PERFORM UNTIL COUNTER2 > 16
               MOVE COUNTER2 TO IN-ID(COUNTER2)
               MOVE B-X-VAR(COUNTER2) TO IN-X(COUNTER2)
               MOVE B-Y-POS(COUNTER2) TO IN-Y(COUNTER2)
               MOVE B-PIECE(COUNTER2) TO IN-NAME(COUNTER2)
               MOVE B-FIRST(COUNTER2) TO IN-FIRST(COUNTER2)

               WRITE MY-RECORD FROM I-INPUT(COUNTER2)

               ADD 1 TO COUNTER2

           END-PERFORM

           CLOSE INFILE
           .
