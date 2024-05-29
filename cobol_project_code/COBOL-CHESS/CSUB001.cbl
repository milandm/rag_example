      ******************************************************************
      * Author:
      * Date:
      * Purpose:
      * Tectonics: cobc
      ******************************************************************
       IDENTIFICATION DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       PROGRAM-ID. CSUB001.
       ENVIRONMENT DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       CONFIGURATION SECTION.
      *-----------------------
       INPUT-OUTPUT SECTION.
      *-----------------------
       DATA DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       FILE SECTION.
      *-----------------------
       WORKING-STORAGE SECTION.

           01 CI-COUNTER PIC 99.
           01 CJ-COUNTER PIC 99.
      *-----------------------
       LINKAGE SECTION.
           COPY COORDINATES.
      *-----------------------
       PROCEDURE DIVISION USING COORDINATES,
           .
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       MAIN-PROCEDURE.

           PERFORM AA-INIT-W-PIECE

           PERFORM AB-INIT-B-PIECE

           GOBACK.

           AA-INIT-W-PIECE SECTION.

      *******************************************************************
      *                     AA-INIT-W-PIECE SECTION                     *
      *******************************************************************

           MOVE 5 TO W-X-VAR(1)
           MOVE 8 TO W-Y-POS(1)
           MOVE 'WK' TO W-PIECE(1)


           MOVE 4 TO W-X-VAR(2)
           MOVE 8 TO W-Y-POS(2)
           MOVE 'WQ' TO W-PIECE(2)

           MOVE 1 TO W-X-VAR(3)
           MOVE 8 TO W-Y-POS(3)
           MOVE 'WR' TO W-PIECE(3)
           MOVE 8 TO W-X-VAR(4)
           MOVE 8 TO W-Y-POS(4)
           MOVE 'WR' TO W-PIECE(4)

           MOVE 2 TO W-X-VAR(5)
           MOVE 8 TO W-Y-POS(5)
           MOVE 'WH' TO W-PIECE(5)
           MOVE 7 TO W-X-VAR(6)
           MOVE 8 TO W-Y-POS(6)
           MOVE 'WH' TO W-PIECE(6)

           MOVE 3 TO W-X-VAR(7)
           MOVE 8 TO W-Y-POS(7)
           MOVE 'WB' TO W-PIECE(7)
           MOVE 6 TO W-X-VAR(8)
           MOVE 8 TO W-Y-POS(8)
           MOVE 'WB' TO W-PIECE(8)

           MOVE 9 TO CI-COUNTER
           MOVE 0 TO CJ-COUNTER


           PERFORM UNTIL CI-COUNTER >= 17
               MOVE 1 TO W-X-VAR(CI-COUNTER)
               ADD CJ-COUNTER TO W-X-VAR(CI-COUNTER)
               MOVE 7 TO W-Y-POS(CI-COUNTER)
               MOVE 'WP' TO W-PIECE(CI-COUNTER)
               ADD 1 TO CJ-COUNTER
               ADD 1 TO CI-COUNTER
           END-PERFORM

           MOVE 1 TO CI-COUNTER

           PERFORM UNTIL CI-COUNTER >= 17
               MOVE 'Y' TO W-FIRST(CI-COUNTER)
               ADD 1 TO CI-COUNTER
           END-PERFORM

           .

           AB-INIT-B-PIECE SECTION.

      *******************************************************************
      *                     AB-INIT-B-PIECE SECTION                     *
      *******************************************************************

           MOVE 5 TO B-X-VAR(1)
           MOVE 1 TO B-Y-POS(1)
           MOVE 'BK' TO B-PIECE(1)

           MOVE 4 TO B-X-VAR(2)
           MOVE 1 TO B-Y-POS(2)
           MOVE 'BQ' TO B-PIECE(2)

           MOVE 1 TO B-X-VAR(3)
           MOVE 1 TO B-Y-POS(3)
           MOVE 'BR' TO B-PIECE(3)
           MOVE 8 TO B-X-VAR(4)
           MOVE 1 TO B-Y-POS(4)
           MOVE 'BR' TO B-PIECE(4)

           MOVE 2 TO B-X-VAR(5)
           MOVE 1 TO B-Y-POS(5)
           MOVE 'BH' TO B-PIECE(5)
           MOVE 7 TO B-X-VAR(6)
           MOVE 1 TO B-Y-POS(6)
           MOVE 'BH' TO B-PIECE(6)

           MOVE 3 TO B-X-VAR(7)
           MOVE 1 TO B-Y-POS(7)
           MOVE 'BB' TO B-PIECE(7)
           MOVE 6 TO B-X-VAR(8)
           MOVE 1 TO B-Y-POS(8)
           MOVE 'BB' TO B-PIECE(8)

           MOVE 9 TO CI-COUNTER
           MOVE 0 TO CJ-COUNTER


           PERFORM UNTIL CI-COUNTER >= 17
               MOVE 1 TO B-X-VAR(CI-COUNTER)
               ADD CJ-COUNTER TO B-X-VAR(CI-COUNTER)
               MOVE 2 TO B-Y-POS(CI-COUNTER)
               MOVE 'BP' TO B-PIECE(CI-COUNTER)
               ADD 1 TO CJ-COUNTER
               ADD 1 TO CI-COUNTER
           END-PERFORM

           MOVE 1 TO CI-COUNTER

           PERFORM UNTIL CI-COUNTER >= 17
               MOVE 'Y' TO B-FIRST(CI-COUNTER)
               ADD 1 TO CI-COUNTER
           END-PERFORM

           .
